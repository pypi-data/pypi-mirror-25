# encoding: utf-8
from __future__ import print_function, division, absolute_import

from functools import partial

import pytest

from datapool.yaml_parsers import parse_parameters
from datapool.database import setup_db, dump_db
from datapool.errors import ConsistencyError
from datapool.parameters_model import check_and_commit
from datapool.pretty_printers import pretty_print

from .yaml_helpers import load

load_parameters = partial(load, parse_parameters)


def test_load_valid_parameters(data_path, regtest, regtest_print, regtest_logger, lz):
    with regtest_logger():
        excs, all_parameters = load_parameters(lz)
    assert not excs, str(excs)
    assert len(all_parameters) == 1
    parameters = all_parameters[0]

    regtest_print("parameter objects read from yaml:")
    for parameter in parameters:
        pretty_print(parameter, file=regtest)


def test_load_empty_parameters(data_path, regtest, regtest_print, regtest_logger, lz):
    lz.overwrite_file("data/parameters.yaml", data_path("yamls/empty.yaml"))

    with regtest_logger():
        excs, __ = load_parameters(lz)

    assert excs
    for exc in excs:
        regtest_print(exc)


def test_load_invalid_parameters(data_path, regtest, regtest_print, regtest_logger, lz):
    lz.overwrite_file("data/parameters.yaml", data_path("yamls/parameters_invalid.yaml"))

    with regtest_logger():
        excs, __ = load_parameters(lz)

    assert excs
    for exc in excs:
        regtest_print(exc)


@pytest.fixture(scope="function")
def setup(data_path, regtest_logger, regtest, regtest_print, config, lz):
    with regtest_logger():
        engine = setup_db(config.db)

    with regtest_logger():
        excs, all_parameters = load_parameters(lz)

    assert not excs, str(excs)
    assert len(all_parameters) == 1
    parameters = all_parameters[0]

    regtest_print("parameters object read from yaml:")
    pretty_print(parameters, file=regtest)

    with regtest_logger():
        return config, engine, check_and_commit(parameters, engine)


def test_commit_valid_parameters(setup, regtest_print, regtest_logger, regtest):
    config, engine, parameter_dbos = setup
    regtest_print()
    for parameter_dbo in parameter_dbos:
        regtest_print("site row:", parameter_dbo)
    regtest_print()
    with regtest_logger():
        dump_db(config.db, file=regtest)


def _inject_and_test(engine, yaml_file, regtest_logger, lz, regtest_print, regtest, config,
                     expect_exception=True):
    lz.overwrite_file("data/parameters.yaml", yaml_file)

    with regtest_logger():
        excs, all_parameters = load_parameters(lz)

    assert not excs, str(excs)
    assert len(all_parameters) == 1
    parameters = all_parameters[0]

    regtest_print("parameters object read from yaml:")
    for parameter in parameters:
        pretty_print(parameter, file=regtest)

    if expect_exception:
        with pytest.raises(ConsistencyError) as e:
            with regtest_logger():
                for dbo in check_and_commit(parameters, engine):
                    print(dbo, file=regtest)
        print(file=regtest)
        print(e.value, file=regtest)
        print(file=regtest)
    else:
        with regtest_logger():
            for dbo in check_and_commit(parameters, engine):
                print(dbo, file=regtest)

    dump_db(config.db, file=regtest)


def test_commit_modified_parameters(setup, data_path, regtest_logger, regtest, regtest_print,
                                    config, lz):
    config, engine, __ = setup
    _inject_and_test(engine,
                     data_path("yamls/parameters_modified.yaml"), regtest_logger, lz,
                     regtest_print, regtest, config)


def test_commit_modified_parameters_2(setup, data_path, regtest_logger, regtest, regtest_print,
                                      config, lz):
    # check allowed updates
    config, engine, __ = setup
    _inject_and_test(engine,
                     data_path("yamls/parameters_modified_2.yaml"), regtest_logger, lz,
                     regtest_print, regtest, config, expect_exception=False)


def test_commit_shortened_parameters(setup, data_path, regtest_logger, regtest, regtest_print,
                                     config, lz):
    config, engine, __ = setup
    _inject_and_test(engine,
                     data_path("yamls/parameters_shortened.yaml"), regtest_logger, lz,
                     regtest_print, regtest, config)
