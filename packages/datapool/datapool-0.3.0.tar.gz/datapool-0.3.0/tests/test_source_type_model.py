# encoding: utf-8
from __future__ import print_function, division, absolute_import

from functools import partial

import pytest

from datapool.yaml_parsers import parse_source_type
from datapool.database import setup_db, dump_db
from datapool.errors import ConsistencyError
from datapool.source_type_model import check_and_commit
from datapool.pretty_printers import pretty_print

from .yaml_helpers import load

load_source_types = partial(load, parse_source_type)


def test_load_valid_source_type(data_path, regtest, regtest_print, regtest_logger, lz):
    with regtest_logger():
        excs, source_types = load_source_types(lz)
    assert not excs, str(excs)
    assert len(source_types) == 1

    regtest_print("source type objects read from yaml:")
    for source_type in source_types:
        pretty_print(source_type, file=regtest)


def test_load_empty_source_type(data_path, regtest, regtest_print, regtest_logger, lz):
    lz.overwrite_file("data/FloDar/source_type.yaml", data_path("yamls/empty.yaml"))

    with regtest_logger():
        excs, __ = load_source_types(lz)

    assert excs
    for exc in excs:
        regtest_print(exc)


def test_load_invalid_source_type(data_path, regtest, regtest_print, regtest_logger, lz):
    lz.overwrite_file("data/FloDar/source_type.yaml", data_path("yamls/source_type_invalid.yaml"))

    with regtest_logger():
        excs, __ = load_source_types(lz)

    assert excs
    for exc in excs:
        regtest_print(exc)


@pytest.fixture(scope="function")
def setup(data_path, regtest_logger, regtest, regtest_print, config, lz):
    with regtest_logger():
        engine = setup_db(config.db)

    with regtest_logger():
        excs, all_source_types = load_source_types(lz)

    assert not excs, str(excs)
    assert len(all_source_types) == 1
    source_type = all_source_types[0]

    regtest_print("source_type object read from yaml:")
    pretty_print(source_type, file=regtest)

    with regtest_logger():
        return config, engine, check_and_commit(source_type, engine)


def test_commit_valid_source_type(setup, regtest_print, regtest_logger, regtest):
    config, engine, source_type_dbos = setup
    regtest_print()
    for source_type_dbo in source_type_dbos:
        regtest_print("site row:", source_type_dbo)
    regtest_print()
    with regtest_logger():
        dump_db(config.db, file=regtest)


def _inject_and_test(engine, yaml_file, regtest_logger, lz, regtest_print, regtest, config,
                     expect_exception=True):
    lz.overwrite_file("data/FloDar/source_type.yaml", yaml_file)

    with regtest_logger():
        excs, source_types = load_source_types(lz)

    assert not excs, str(excs)
    assert len(source_types) == 1
    source_type = source_types[0]

    regtest_print("source_type object read from yaml:")
    pretty_print(source_type, file=regtest)

    def test_check_and_commit(*a):
        for dbo in check_and_commit(*a):
            print(dbo, file=regtest)

    if expect_exception:
        with pytest.raises(ConsistencyError) as e:
            with regtest_logger():
                test_check_and_commit(source_type, engine)

            print(file=regtest)
            print(e.value, file=regtest)
            print(file=regtest)

    else:
        test_check_and_commit(source_type, engine)

    dump_db(config.db, file=regtest)


def test_commit_modified_source_types(setup, data_path, regtest_logger, regtest, regtest_print,
                                      config, lz):
    config, engine, __ = setup
    _inject_and_test(engine,
                     data_path("yamls/source_type_modified.yaml"), regtest_logger, lz,
                     regtest_print, regtest, config)

def test_commit_source_types_with_allowed_modifications(setup, data_path, regtest_logger, regtest,
                                                        regtest_print, config, lz):
    config, engine, __ = setup
    _inject_and_test(engine,
                     data_path("yamls/source_type_allowed_modifications.yaml"), regtest_logger, lz,
                     regtest_print, regtest, config, expect_exception=False)
