# encoding: utf-8
from __future__ import print_function, division, absolute_import

from datapool.database import setup_db, dump_db
from datapool.dispatcher import Dispatcher, log_unexpected_exceptions
from datapool.utils import find_executable
from datapool.logger import logger


def test_log_unexpected_exceptions(regtest_logger):
    @log_unexpected_exceptions
    def by_zero(a, b, c):
        return a + b / c

    with regtest_logger():
        by_zero(1, 2, 0)
        by_zero("1", 2, c=0)
        by_zero({1}, b="2", c=0)


def _run_dispatcher(config, regtest_logger, lz, pathes):
    setup_db(config.db)
    with regtest_logger():
        dispatcher = Dispatcher(config, time_provider=lambda: "NOW")
        for path in pathes:
            for message in dispatcher.dispatch(path):
                logger().info("message: {}".format(message))


def test_dispatcher_ok(config, regtest, regtest_logger, lz):
    pathes = (
        "sites/example_site/site.yaml",
        "data/parameters.yaml",
        "data/FloDar/source_type.yaml",
        "data/FloDar/FloDar_python/source.yaml",
        "data/FloDar/FloDar_python/conversion.py",
        "data/FloDar/FloDar_python/raw_data/data-001.raw", )

    config.python.executable = find_executable("python")
    _run_dispatcher(config, regtest_logger, lz, pathes)
    dump_db(config.db, file=regtest, max_rows=25)


def test_dispatcher_no_python(config, regtest_logger, lz):
    # we don't configure r here to trigger an error
    pathes = ("data/FloDar/FloDar_python/conversion.py",
              "data/FloDar/FloDar_python/raw_data/data-001.raw")

    _run_dispatcher(config, regtest_logger, lz, pathes)


def test_dispatcher_no_raw(config, regtest_logger, lz):
    lz.remove_file("data/FloDar/FloDar_python/raw_data/data-001.raw")
    pathes = ("data/FloDar/FloDar_python/conversion.py", )
    _run_dispatcher(config, regtest_logger, lz, pathes)


def test_dispatcher_no_script(config, regtest_logger, lz):
    lz.remove_file("data/FloDar/FloDar_python/conversion.py")
    pathes = ("data/FloDar/FloDar_python/raw_data/data-001.raw", )
    _run_dispatcher(config, regtest_logger, lz, pathes)


def test_dispatcher_multiple_scripts(config, regtest_logger, lz):
    lz.overwrite_file("data/FloDar/FloDar_python/conversion.jl",
                      lz.p("data/FloDar/FloDar_python/conversion.py"))
    pathes = ("data/FloDar/FloDar_python/raw_data/data-001.raw", )
    _run_dispatcher(config, regtest_logger, lz, pathes)


def test_dispatcher_wrong_yaml_name(config, regtest_logger, lz):
    pathes = ("data/invalid_name.yaml", )
    _run_dispatcher(config, regtest_logger, lz, pathes)


def test_dispatcher_invalid_yaml(config, regtest_logger, data_path, lz):
    lz.overwrite_file("data/parameters.yaml", data_path("yamls/empty.yaml"))
    pathes = ("data/parameters.yaml", )
    _run_dispatcher(config, regtest_logger, lz, pathes)
