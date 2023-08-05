# encoding: utf-8
from __future__ import print_function, division, absolute_import
"""this module holds the configuration of the folder structure of the landing zone and
corresponding functions.

All modifications to the landing zone structure should be implemented here to have one single point
of configuration.

"""

from collections import namedtuple
from functools import partial
import fnmatch
import glob
import os.path

scripts_pattern = "data/*/*/conversion.*"
lock_file = ".write_lock"

Handler = namedtuple("Handler", ["parser", "checker", "committer"])


def ordered_fnmatch_patterns_for_update():
    """ordered list of glob patterns. order is important

    1. images
    2. sites
    3. source_types
    4. sources
    6. conversion scripts
    5. raw data
    """
    yield "sites/*/images/*"

    for pattern, __ in config():
        yield pattern

    from .data_conversion import SUPPORTED_EXTENSIONS
    for extension in sorted(SUPPORTED_EXTENSIONS):
        yield "data/*/*/conversion{}".format(extension)

    yield "data/*/*/raw_data/data-*.raw"


def config():
    from .yaml_parsers import parse_parameters, parse_site, parse_source_type, parse_source

    from .site_and_picture_model import check, check_and_commit
    yield "sites/*/site.yaml", Handler(parse_site, check, check_and_commit)

    from .parameters_model import check, check_and_commit
    yield "data/parameters.yaml", Handler(parse_parameters, check, check_and_commit)

    from .source_type_model import check, check_and_commit
    yield "data/*/source_type.yaml", Handler(parse_source_type, check, check_and_commit)

    from .source_model import check, check_and_commit
    yield "data/*/*/source.yaml", Handler(parse_source, check, check_and_commit)


def raw_file_pattern_for_script(script_path):
    folder = os.path.dirname(script_path)
    return os.path.join(folder, "raw_data", "data-*.raw")


def script_paths_for_raw_file(raw_file_path):
    folder = os.path.dirname(raw_file_path)
    parent_folder, __ = os.path.split(folder)
    pattern = os.path.join(parent_folder, "conversion.*")
    return glob.glob(pattern)


def source_yaml_path_for_script(script_path):
    folder = os.path.dirname(script_path)
    return os.path.join(folder, "source.yaml")


def source_type_yaml_for_source_yaml(source_yaml_path):
    folder = os.path.dirname(source_yaml_path)
    parent_folder, __ = os.path.split(folder)
    return os.path.join(parent_folder, "source_type.yaml")


"""
About mapping patterns,  parsers, checkers:

We use lazy initialization below to offer one single place of configuration without any circular
imports.

We could implement a class, but this would have only one instance which we only offer static
methods or would make use of the singleton pattern.  Instead we implement simple functions and
carefully use two global variables.

(If you consider modules and object / classes as namespaces both approaches are the same on a
conceptual level, only the syntax differs).
"""

_patterns_and_checkers = None
_inverted_patterns = None


def _setup():
    global _patterns_and_checkers
    global _inverted_patterns
    _patterns_and_checkers = []
    _inverted_patterns = {}
    for pattern, handler in config():
        _patterns_and_checkers.append((pattern, handler))
        _inverted_patterns[handler.parser] = pattern


def lookup_handler(rel_path):

    # to improve lookup speed
    if not rel_path.endswith(".yaml"):
        return None

    if _patterns_and_checkers is None:
        _setup()
    for pattern, handler in _patterns_and_checkers:
        if fnmatch.fnmatch(rel_path, pattern):
            return handler

    return None


def _lookup(attribute, rel_path):
    handler = lookup_handler(rel_path)
    if handler is not None:
        return getattr(handler, attribute)


lookup_parser = partial(_lookup, "parser")
lookup_checker = partial(_lookup, "checker")
lookup_committer = partial(_lookup, "committer")


def lookup_pattern(parser):
    if _inverted_patterns is None:
        _setup()
    return _inverted_patterns.get(parser)
