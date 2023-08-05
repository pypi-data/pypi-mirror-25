# encoding: utf-8
from __future__ import print_function, division, absolute_import

import contextlib
import inspect
import logging
import logging.config
import os.path

import yaml


def resolve_logger_config_path(config):
    config_file = config.logging.config_file
    if not os.path.isabs(config_file):
        folder = os.path.dirname(config.__file__)
        config_file = os.path.join(folder, config_file)
    return config_file


def _setup_logger_from(config_file):

    with open(config_file, "r") as fh:
        config = yaml.load(fh)

    logging.config.dictConfig(config)
    logger = logging.getLogger("eawag.datapool")
    return logger


def check_logging_config(config):

    config_file = resolve_logger_config_path(config)

    with open(config_file, "r") as fh:
        config = yaml.load(fh)

    # direct setting a logger is not supported by the logging api, instead
    # we later reset the __dict__ of the maybe existing eawag.datapool logger:
    orig_attributes = logging.getLogger("eawag.datapool").__dict__.copy()

    logging.config.dictConfig(config)

    # as said, setting is not supported, so we updat / overwrite the __dict__ with
    # the attributes of the logger:
    logging.getLogger("eawag.datapool").__dict__.update(orig_attributes)


def _setup_logger(config):
    config_file = resolve_logger_config_path(config)
    logger = _setup_logger_from(config_file)
    return logger


class _LoggerSingleton:

    logger = None
    call_frames = []

    @classmethod
    def setup_logger(clz, config):
        if clz.logger is not None:
            clz._handle_error()
        call_frame = inspect.stack()[1]
        clz.logger = _setup_logger(config)
        clz.call_frames.append(call_frame)

    @classmethod
    def setup_logger_from(clz, config_file):
        if clz.logger is not None:
            clz._handle_error()
        call_frame = inspect.stack()[1]
        clz.logger = _setup_logger_from(config_file)
        clz.call_frames.append(call_frame)

    @classmethod
    def _handle_error(clz):
        infos = ["{f.filename}({f.lineno}): {f.function}".format(f=f) for f in clz.call_frames]
        msg = "logger was already set in this order:\n" + "\n".join(infos)
        raise RuntimeError(msg)

    @classmethod
    def get_logger(clz):
        assert clz.logger is not None, "you have to setup the logger first"
        assert clz.logger.name == "eawag.datapool", clz.logger.name
        return clz.logger

    @classmethod
    def drop_logger(clz):
        clz.logger = None
        clz.call_frames = []

    @classmethod
    @contextlib.contextmanager
    def replace_handlers(clz, handler):
        assert clz.logger is not None, "you have to setup the logger first"
        handlers = clz.logger.handlers[:]
        clz.logger.handlers[:] = [handler]
        yield
        clz.logger.handlers[:] = handlers


setup_logger = _LoggerSingleton.setup_logger
setup_logger_from = _LoggerSingleton.setup_logger_from

drop_logger = _LoggerSingleton.drop_logger
logger = _LoggerSingleton.get_logger

replace_handlers = _LoggerSingleton.replace_handlers
