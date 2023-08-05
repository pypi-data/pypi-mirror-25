# encoding: utf-8
from __future__ import print_function, division, absolute_import

import sys

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine import reflection
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

from .db_objects import Base, declarative_base
from .errors import InvalidOperationError
from .utils import hexdigest, print_table
from .logger import logger


def connect_to_db(db_config, *, verbose=False):

    if db_config.connection_string.startswith("sqlite"):
        from sqlite3 import dbapi2 as sqlite
        engine = create_engine(db_config.connection_string, module=sqlite, echo=verbose)
    else:
        engine = create_engine(db_config.connection_string, echo=verbose)
    try:
        engine.connect()
    except exc.OperationalError as e:
        raise InvalidOperationError("could not connect to {}. Error is {}".format(
            db_config.connection_string, e)) from None
    l = logger()
    l.info("connected to db {}".format(db_config.connection_string))
    return engine


def create_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    # we yield dbos which usually get invalid (expire) after commit, then attributes can not be
    # accessed any more and eg pretty_printing in tests fails. we disable this:
    session.expire_on_commit = False
    return session


def setup_db(db_config, *, verbose=False):
    """creates tables in database"""
    if check_if_tables_exist(db_config):
        raise InvalidOperationError("use setup_fresh_db, the tables in {!r} already exist".format(
            db_config.connection_string))
    engine = connect_to_db(db_config, verbose=verbose)
    Base.metadata.create_all(engine)
    logger().info("created all tables of db {}".format(db_config.connection_string))
    return engine


def check_if_tables_exist(db_config, *, verbose=False):
    engine = connect_to_db(db_config, verbose=verbose)
    declared_names = Base.metadata.tables.keys()
    existing_names = reflection.Inspector.from_engine(engine).get_table_names()
    return bool(set(declared_names) & set(existing_names))


def setup_fresh_db(db_config, *, verbose=False):
    """creates tables in database, deletes already existing data if present"""
    if not check_if_tables_exist(db_config):
        raise InvalidOperationError("use setup_db, the tables in {!r} do not exist".format(
            db_config.connection_string))
    engine = connect_to_db(db_config, verbose=verbose)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logger().info("droped and created all tables of db {}".format(db_config.connection_string))
    return engine


def copy_db(db_config_source,
            db_config_destination,
            *,
            delete_existing,
            copy_signals,
            verbose=False):
    logger().info("copy tables {} -> {}".format(db_config_source.connection_string,
                                                db_config_destination.connection_string))
    engine_source = connect_to_db(db_config_source, verbose=verbose)
    engine_destination = connect_to_db(db_config_destination, verbose=verbose)

    table_names_source = reflection.Inspector.from_engine(engine_source).get_table_names()
    existing_names_destination = reflection.Inspector.from_engine(
        engine_destination).get_table_names()

    if set(table_names_source) & set(existing_names_destination):
        if not delete_existing:
            raise InvalidOperationError("can not copy {} -> {}, some tables already exist on "
                                        "target db".format(db_config_source.connection_string,
                                                           db_config_destination.connection_string))
    if delete_existing or not set(table_names_source) & set(existing_names_destination):
        Base.metadata.drop_all(engine_destination)
        Base.metadata.create_all(engine_destination)

    for table_name in sorted(table_names_source):
        # TODO: import Dbo from db_objects.py and use the configure table name:
        # TODO: write test
        if table_name == "signal" and not copy_signals:
            continue
        yield table_name
        _copy_table(engine_source, engine_destination, table_name, delete_existing, verbose)


def _copy_table(engine_source, engine_destination, table_name, delete_existing, verbose):
    source = sessionmaker(bind=engine_source)()
    destination = sessionmaker(bind=engine_destination)()

    source_meta = MetaData(bind=engine_source)

    logger().info("copy schema of table {}".format(table_name))

    table = Table(table_name, source_meta, autoload=True)

    Base = declarative_base()

    class NewRecord(Base):
        __table__ = table

    columns = table.columns.keys()
    logger().info("copy rows of table {}".format(table_name))
    for record in source.query(table).all():
        data = dict([(str(column), getattr(record, column)) for column in columns])
        destination.merge(NewRecord(**data))

    logger().info("commit changes for table {}".format(table_name))
    destination.commit()


def _dump_table(engine, source, source_meta, table_name, indent="", file=sys.stdout, max_rows=None):
    table = Table(table_name, source_meta, autoload=True)
    columns = table.columns.keys()
    rows = []
    for record in source.query(table).all():
        row = []
        for column in columns:
            data = getattr(record, column)
            if isinstance(data, bytes):
                data = hexdigest(data)
            row.append(data)
        rows.append(row)
    print_table(columns, rows, indent=indent, file=file, max_rows=max_rows)


def dump_db(db_config, file=sys.stdout, max_rows=None):
    engine = connect_to_db(db_config)
    source = sessionmaker(bind=engine)()
    source_meta = MetaData(bind=engine)
    table_names = reflection.Inspector.from_engine(engine).get_table_names()
    for table_name in table_names:
        print("table {}:".format(table_name), file=file)
        print(file=file)
        _dump_table(
            engine, source, source_meta, table_name, indent="   ", file=file, max_rows=max_rows)
        print(file=file)
