# encoding: utf-8
from __future__ import print_function, division, absolute_import

from collections import Counter
import datetime
import operator

from sqlalchemy.orm import sessionmaker

from .converters import domain_object_to_dbo
from .domain_objects import Signal
from .errors import ConsistencyError, DataPoolException
from .db_objects import SiteDbo, ParameterDbo, SourceDbo, SignalDbo
from .utils import iter_to_list, is_number


def _check_fields(signal):
    assert isinstance(signal, Signal)

    if not isinstance(signal.timestamp, datetime.datetime):
        yield "'{}' is not a datetime object".format(signal.timestamp)

    if not is_number(signal.value):
        yield "'{}' is not a number".format(signal.value)

    if not signal.parameter:
        yield "parameter field is empty"

    if "site" in signal:
        if not signal.site:
            yield "site field is empty"

    for name in ("x", "y", "z"):
        v = signal.get(name)
        if v is not None:
            if v != "":
                if not is_number(v):
                    yield "value '{}' in field {} is not valid".format(v, name)


def check_fields(signals):
    for (i, signal) in enumerate(signals):
        for msg in _check_fields(signal):
            yield "(row {}) {}".format(i, msg)


class Context:

    def __init__(self, engine):
        self.session = sessionmaker(bind=engine)()
        self.source_name_to_id = None
        self.parameter_name_to_id = None
        self.site_name_to_id = None
        self.site_name_to_coordinates = None

    @property
    def query(self):
        return self.session.query

    @property
    def add(self):
        return self.session.add

    @property
    def commit(self):
        return self.session.commit

    def get_source_id(self, source_name):
        if self.source_name_to_id is None:
            self.load()
        return self.source_name_to_id.get(source_name)

    def get_parameter_id(self, parameter_name):
        if self.parameter_name_to_id is None:
            self.load()
        return self.parameter_name_to_id.get(parameter_name)

    def get_site_id(self, site_name):
        if self.site_name_to_id is None:
            self.load()
        return self.site_name_to_id.get(site_name)

    def get_site_coordinates(self, site_name):
        if self.site_name_to_coordinates is None:
            self.load()
        return self.site_name_to_coordinates.get(site_name)

    def load(self):
        self.source_name_to_id = {}
        q = self.query(SourceDbo.name, SourceDbo.source_id)
        for name, id_ in q.all():
            self.source_name_to_id[name] = id_

        self.parameter_name_to_id = {}
        q = self.query(ParameterDbo.name, ParameterDbo.parameter_id)
        for name, id_ in q.all():
            self.parameter_name_to_id[name] = id_

        self.site_name_to_id = {}
        self.site_name_to_coordinates = {}

        q = self.query(SiteDbo)
        for site in q.all():
            self.site_name_to_id[site.name] = site.site_id
            self.site_name_to_coordinates[site.name] = (site.coord_x, site.coord_y, site.coord_z)


def check_and_commit(signals, engine):
    context = Context(engine)
    exceptions = check_signals_against_db(signals, engine, context)
    if exceptions:
        raise ConsistencyError("check for signals failed, see logs for details")
    return commit(signals, engine, context)


@iter_to_list
def check_signals_against_db(signals, engine, context=None):

    if context is None:
        context = Context(engine)

    signals_to_check = []
    for result in check_existing_fields(signals, context):
        if isinstance(result, ConsistencyError):
            yield result
        else:
            signals_to_check.append(result)

    if not signals_to_check:
        return

    for signal, exact_match in check_existing_signals(signals_to_check, context):
        dimensions = "'{}', '{}', '{}'".format(signal.source, signal.parameter,
                                               signal.timestamp)
        if not exact_match:
            msg = "signal for ({}) having value {} already in db".format(dimensions, signal.value)
            yield ConsistencyError(msg)


@iter_to_list
def check_signals_uniqueness(signals):

    timestamps = [s.timestamp for s in signals]
    source_names = [s.source for s in signals]
    parameter_names = [s.parameter for s in signals]
    values = [s.value for s in signals]
    coordinates = zip(timestamps, source_names, parameter_names, values)

    counts = Counter(coordinates)

    for (coordinate, count) in counts.most_common():
        if count == 1:
            break
        dt, source_name, parameter_name, value = coordinate
        c_str = "{}, {}, {}, {}".format(dt.strftime('%Y-%m-%d %H:%M:%S'),
                                        source_name, parameter_name, value)
        yield ConsistencyError("duplicate signal ({}) found {} times".format(c_str, count))


def check_existing_fields(signals, context):
    """we check if entries source and parameter in given signals are defined in database"""

    reported_sources = set()
    reported_parameters = set()
    reported_sites = set()

    for signal in signals:
        parameter_name = signal.parameter
        source_name = signal.source
        source_id = context.get_source_id(source_name)
        parameter_id = context.get_parameter_id(parameter_name)

        if source_id is None and source_name not in reported_sources:
            yield ConsistencyError("source '{}' does not exist in db".format(source_name))
            reported_sources.add(source_name)

        if parameter_id is None and parameter_name not in reported_parameters:
            yield ConsistencyError("parameter '{}' does not exist in db".format(parameter_name))
            reported_parameters.add(parameter_name)

        site = signal.get("site")
        site_id = -1
        if site is not None:
            site_id = context.get_site_id(site)
            if site_id is None and site not in reported_sites:
                yield ConsistencyError("site '{}' does not exist in db".format(site))
                reported_sites.add(site)

        if source_id is not None and parameter_id is not None and site_id is not None:
            yield signal


def check_existing_signals(signals, context):
    """we check if signals already exist in database.
       for signals the tuple (timestamp, parameter, source) must be unqiue"""

    getter = operator.attrgetter

    def list_map(function, iterable):
        return list(map(function, iterable))

    timestamps = list_map(getter("timestamp"), signals)
    source_names = list_map(getter("source"), signals)
    parameter_names = list_map(getter("parameter"), signals)

    # fast query, but will produce false positives !
    source_ids = list_map(context.get_source_id, source_names)
    parameter_ids = list_map(context.get_parameter_id, parameter_names)

    min_ts = min(timestamps)
    max_ts = max(timestamps)
    q = context.query(SignalDbo.timestamp, SignalDbo.source_id, SignalDbo.parameter_id,
                      SignalDbo.value)
    q = q.filter(
        SignalDbo.source_id.in_(set(source_ids)),
        SignalDbo.parameter_id.in_(set(parameter_ids)),
        SignalDbo.timestamp.between(min_ts, max_ts))

    possible_matches = q.all()

    if not possible_matches:
        return

    # index: map unique key / "dimension" to signal:
    dimensions = zip(timestamps, source_ids, parameter_ids)
    dimension_to_signal = dict(zip(dimensions, signals))

    for match in possible_matches:
        dimension = match[:-1]
        value = match[-1]
        if dimension in dimension_to_signal:
            signal = dimension_to_signal[dimension]
            yield dimension_to_signal[dimension], signal.value == value


def commit(signals, engine, context=None):
    if context is None:
        context = Context(engine)

    signals_for_db = []
    for signal in signals:
        signal = signal.copy()

        signal.parameter_id = context.get_parameter_id(signal.parameter)
        del signal.parameter

        signal.source_id = context.get_source_id(signal.source)
        del signal.source

        if "site" in signal:
            signal.site_id = context.get_site_id(signal.site)
            coord = context.get_site_coordinates(signal.site)
            if coord is not None:
                x, y, z = coord
                signal.coord_x = str(x)
                signal.coord_y = str(y)
                signal.coord_z = str(z)
            del signal.site
        else:
            signal.coord_x = signal.x
            signal.coord_y = signal.y
            signal.coord_z = signal.z
            del signal.x
            del signal.y
            del signal.z
        signals_for_db.append(signal)

    for signal in signals_for_db:
        signal = domain_object_to_dbo(signal)
        context.add(signal)
    context.commit()
