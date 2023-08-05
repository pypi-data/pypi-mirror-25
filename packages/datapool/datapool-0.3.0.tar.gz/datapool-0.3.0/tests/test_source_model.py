# encoding: utf-8
from __future__ import print_function, division, absolute_import

from functools import partial

import pytest

from datapool.yaml_parsers import parse_source, parse_source_type, parse_parameters
from datapool.database import setup_db, dump_db
from datapool.errors import ConsistencyError
from datapool.source_model import check_and_commit, check
from datapool.pretty_printers import pretty_print

from .yaml_helpers import load

load_parameters = partial(load, parse_parameters)
load_source = partial(load, parse_source)
load_source_type = partial(load, parse_source_type)


def test_load_valid_source(data_path, regtest, regtest_print, regtest_logger, lz):
    with regtest_logger():
        excs, sources = load_source(lz)
    assert len(sources) == 1, excs
    source = sources[0]
    regtest_print("source object read from yaml:")
    pretty_print(source, file=regtest)
    assert not excs, str(excs)


def test_load_empty_source_yml(data_path, regtest_print, regtest_logger, lz):
    lz.overwrite_file("data/FloDar/FloDar_python/source.yaml", data_path("yamls/empty.yaml"))

    with regtest_logger():
        excs, sources = load_source(lz)

    assert not sources
    assert excs
    for exc in excs:
        regtest_print(exc)


def test_load_invalid_source_yml(data_path, regtest_print, regtest_logger, lz):
    lz.overwrite_file("data/FloDar/FloDar_python/source.yaml",
                      data_path("yamls/source_invalid.yaml"))

    with regtest_logger():
        excs, sources = load_source(lz)

    assert not sources
    assert excs
    for exc in excs:
        regtest_print(exc)


@pytest.fixture(scope="function")
def engine(config, lz):
    from datapool.parameters_model import check_and_commit as check_and_commit_parameters
    from datapool.source_type_model import check_and_commit as check_and_commit_st

    __, (parameters,) = load_parameters(lz)
    engine = setup_db(config.db)
    check_and_commit_parameters(parameters, engine)

    excs, (source_type, ) = load_source_type(lz)
    assert not excs

    check_and_commit_st(source_type, engine)
    return engine


def test_commit_valid_source(data_path, regtest_logger, regtest, regtest_print, config, lz, engine):

    with regtest_logger():
        excs, (source, ) = load_source(lz)
        assert not excs

    regtest_print("source object read from yaml:")
    pretty_print(source, file=regtest)

    with regtest_logger():
        for source_dbo in  check_and_commit(source, engine):
            regtest_print()
            regtest_print("source row:", source_dbo)
            pretty_print(source_dbo, file=regtest)
            regtest_print()

    dump_db(config.db, file=regtest)


def test_commit_invalid_source_yml(data_path, regtest_print, regtest_logger, lz, config):
    from datapool.parameters_model import check_and_commit as check_and_commit_parameters

    __, (parameters,) = load_parameters(lz)

    engine = setup_db(config.db)
    check_and_commit_parameters(parameters, engine)

    lz.overwrite_file("data/FloDar/FloDar_python/source.yaml",
                      data_path("yamls/source_unknown_parameters.yaml"))

    excs, sources = load_source(lz)

    with regtest_logger():
        for e in check(sources[0], engine):
            regtest_print(e)


def test_update_modified_source_yml(data_path, regtest, regtest_logger, config, lz, engine):

    def setup():
        excs, (source, ) = load_source(lz)
        assert not excs, str(excs)

        print("source object read from yaml:", file=regtest)
        pretty_print(source, file=regtest)
        print(file=regtest)

        with regtest_logger():
            for source_dbo in check_and_commit(source, engine):
                print("source row after update:", source_dbo, file=regtest)
                pretty_print(source_dbo, file=regtest)
                print(file=regtest)

    setup()

    lz.overwrite_file("data/FloDar/FloDar_python/source.yaml",
                      data_path("yamls/source_averaging_added.yaml"))
    with regtest_logger():
        excs, (source, ) = load_source(lz)
    assert not excs, str(excs)

    print("source object read from yaml:", file=regtest)
    pretty_print(source, file=regtest)

    # modified source should work:
    with regtest_logger():
        for dbo in check_and_commit(source, engine):
            print(dbo, file=regtest)

    # load a modified (but syntactically valid) source.yaml
    lz.overwrite_file("data/FloDar/FloDar_python/source.yaml",
                      data_path("yamls/source_modified.yaml"))
    with regtest_logger():
        excs, (source,) = load_source(lz)
    assert not excs, str(excs)

    print("source object read from yaml:", file=regtest)
    pretty_print(source, file=regtest)

    # modified source should not raise errors:
    for dbo in check_and_commit(source, engine):
        print(dbo, file=regtest)

    # invalid modification
    source.averaging[0].parameter = "was_Temperatur"

    with pytest.raises(ConsistencyError) as e:
        with regtest_logger():
            check_and_commit(source, engine)
        print(file=regtest)
        print(e.value, file=regtest)
        print(file=regtest)

    dump_db(config.db, file=regtest)
