# encoding: utf-8
from __future__ import print_function, division, absolute_import

from datapool.database import setup_db, dump_db
from datapool.db_objects import ParameterDbo, SourceDbo, SourceTypeDbo, SiteDbo
from datapool.domain_objects import Signal
from datapool.errors import DataPoolException
from datapool.signal_model import check_signals_against_db, commit, check_and_commit
from datapool.uniform_file_format import parse_timestamp
from datapool.utils import iter_to_list

from sqlalchemy.orm import sessionmaker

import pytest


@pytest.fixture
@iter_to_list
def signals():
    for d in range(3):
        dt = "{:4d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(2015, 12, d + 1, 12 + d, 11, 12)
        dt = parse_timestamp(dt)
        yield Signal(
            dict(
                timestamp=dt,
                site="example_site",
                source="example_source",
                parameter="temperature",
                value=float(-3 + d))
            )

        yield Signal(
            dict(
                timestamp=dt,
                x=1,
                y=2,
                z=3,
                source="example_source",
                parameter="wind speed",
                value=float(10 + 10 * d))
            )


@pytest.fixture(scope="function")
def engine(config, setup_logger):
    engine = setup_db(config.db)
    return engine


def setup_valid_db(engine):

    session = sessionmaker(bind=engine)()
    session.add(ParameterDbo(name="wind speed", description="", unit="km/h"))
    session.add(ParameterDbo(name="temperature", description="", unit="C"))
    site = SiteDbo(name="example_site", description="", street="", postcode="666", city="hell",
                   coord_x=111, coord_y=222)
    session.add(site)
    source_type = SourceTypeDbo(name="example_source_type")
    session.add(source_type)
    session.add(SourceDbo(name="example_source", serial="000000", source_type=source_type))
    session.commit()


def test_check_signals_against_empty_db(signals, engine, config, regtest):

    for msg in check_signals_against_db(signals, engine):
        print(msg, file=regtest)


def test_check_signals_against_valid_db(signals, engine, config, regtest):

    setup_valid_db(engine)

    for msg in check_signals_against_db(signals, engine):
        assert False, "should not happen: {}".format(msg)

    commit(signals, engine)
    dump_db(config.db, file=regtest)

    assert not check_signals_against_db(signals, engine)


def test_check_and_commit(signals, engine, config, regtest):

    setup_valid_db(engine)

    check_and_commit(signals, engine)
    dump_db(config.db, file=regtest)
    assert not check_signals_against_db(signals, engine)

    for s in signals[:3]:
        s.value += 1
    dump_db(config.db, file=regtest)

    for msg in check_signals_against_db(signals, engine):
        print(msg, file=regtest)

    with pytest.raises(DataPoolException):
        check_and_commit(signals, engine)

    dump_db(config.db, file=regtest)
