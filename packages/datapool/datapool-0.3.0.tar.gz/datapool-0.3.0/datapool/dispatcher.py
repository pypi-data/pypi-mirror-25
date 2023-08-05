# encoding: utf-8
from __future__ import print_function, division, absolute_import

from datetime import datetime
import functools
import os
import shutil
import time

from .database import connect_to_db
from .data_conversion import ConversionRunner, SUPPORTED_EXTENSIONS
from .errors import DataPoolException, InvalidOperationError
from .domain_objects import DomainObject
from .landing_zone_structure import (lookup_handler, script_paths_for_raw_file,
                                     source_yaml_path_for_script)

from .logger import logger
from .signal_model import commit as commit_signals, check_signals_against_db
from .uniform_file_format import to_signals
from .utils import iter_to_list
from .yaml_parsers import parse_source


def log_unexpected_exceptions(function):
    @functools.wraps(function)
    def wrapped_function(*a, **kw):
        logger()
        try:
            return function(*a, **kw)
        except Exception as e:
            args = list("{!r}".format(arg) for arg in a)
            args += list("{}={!r}".format(k, v) for (k, v) in sorted(kw.items()))
            call_signature = "{}({})".format(function.__name__, ", ".join(args))
            logger().error("unexpected error '{}' when calling {}".format(e, call_signature))

    return wrapped_function


def default_time_provider():
    return datetime.now().strftime("%Y%m%d-%H%M%S-%f")


class Dispatcher:

    def __init__(self, config, time_provider=default_time_provider):
        """
        time_provider arg allows patching for regression tests !
        """
        self.config = config
        self.time_provider = time_provider
        self.root_folder = config.landing_zone.folder
        self.conversion_runner = ConversionRunner(config)
        self.engine = connect_to_db(self.config.db)

    @iter_to_list
    def dispatch(self, rel_path):
        if rel_path.endswith(".yaml"):
            yield from self.dispatch_yaml(rel_path)
        elif rel_path.endswith(".raw"):
            yield from self.dispatch_raw_file_conversion(rel_path)
        elif any(rel_path.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            # no dispatch because dispatch is triggered on .raw file creation, only backup:
            yield from self.backup(rel_path)
        else:
            yield "do not know how to process file {}".format(rel_path)

    def backup(self, rel_path):
        try:
            yield from self._backup(rel_path)
        except IOError as e:
            yield "backup of {} failed: {}".format(rel_path, e)

    def _backup(self, rel_path):
        backup_path = os.path.join(self.config.backup_landing_zone.folder, rel_path)
        folder = os.path.dirname(backup_path)
        if not os.path.exists(folder):
            os.makedirs(folder)
            yield "created folder {}".format(folder)

        # add time stamp to make file unique and better searchable:
        backup_path += ".{}".format(self.time_provider())

        shutil.copy(self.full_path(rel_path), backup_path)
        yield "copied {} to {}".format(rel_path, backup_path)

    def full_path(self, *a):
        return os.path.join(self.root_folder, *a)

    def rel_path(self, p):
        return os.path.relpath(p, self.root_folder)

    def dispatch_raw_file_conversion(self, rel_raw_file_path):
        raw_file_path = self.full_path(rel_raw_file_path)
        script_paths = script_paths_for_raw_file(raw_file_path)

        if len(script_paths) > 1:
            yield InvalidOperationError("multiple conversion scripts found for {}"
                                        .format(rel_raw_file_path))
            return

        if len(script_paths) == 0:
            yield InvalidOperationError("no conversion script found next to {}"
                                        .format(rel_raw_file_path))
            return

        yield from self.run_conversion(script_paths[0], raw_file_path)
        yield from self.backup(rel_raw_file_path)

    def run_conversion(self, script_path, raw_file_path):
        rel_script_path = self.rel_path(script_path)
        rel_raw_file_path = self.rel_path(raw_file_path)

        msg = "convert {} with {}".format(rel_raw_file_path, rel_script_path)
        yield msg
        logger().info(msg)

        started = time.time()
        try:
            rows = self.conversion_runner.run_conversion(script_path, raw_file_path)
        except DataPoolException as e:
            msg = "converting {} with {} failed: '{}'".format(rel_raw_file_path, rel_script_path, e)
            yield msg
            logger().error(msg)
            return
        needed = time.time() - started

        msg = "timing: converting {} needed {:.2f} seconds".format(rel_raw_file_path, needed)
        yield msg
        logger().info(msg)

        source = next(parse_source(self.root_folder, source_yaml_path_for_script(script_path)))
        for row in rows:
            row["source"] = source.name

        started = time.time()
        signals = to_signals(rows)
        errors = check_signals_against_db(signals, self.engine)
        if errors:
            MAXE = 50
            too_many = len(errors) > MAXE
            orig_len = len(errors)
            errors = errors[:MAXE]
            for e in errors:
                msg = "converting {} with {} failed: '{}'".format(rel_raw_file_path,
                                                                  rel_script_path, e)
                yield InvalidOperationError(msg)
                logger().error(msg)
            if too_many:
                msg = "skipped {} error messages".format(orig_len - MAXE)
                yield InvalidOperationError(msg)

            return
        msg = "checked {} signals, needed {:.2f} seconds".format(len(signals), needed)
        yield msg
        logger().info(msg)

        started = time.time()
        commit_signals(signals, self.engine)
        needed = time.time() - started
        msg = "commited {} signals, needed {:.2f} seconds".format(len(signals), needed)
        logger().info(msg)
        yield msg

    def dispatch_yaml(self, rel_path):
        handler = lookup_handler(rel_path)

        if handler is None:
            yield InvalidOperationError("don't know how to handle {}".format(rel_path))
            return

        ok = True
        domain_object = None
        for result in handler.parser(self.root_folder, rel_path):
            if isinstance(result, DomainObject):
                domain_object = result
                continue
            yield InvalidOperationError("when parsing {}: {}".format(rel_path, result))
            ok = False

        if not ok:
            return

        if domain_object is None:
            yield "nothing to commit"
            return

        try:
            committed = handler.committer(domain_object, self.engine)
            if committed:
                yield "commited changes"
            else:
                yield "nothing committed, possibly no update"
        except DataPoolException as e:
            yield e

        self.backup(rel_path)
