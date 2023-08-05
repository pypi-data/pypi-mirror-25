# encoding: utf-8
from __future__ import print_function, division, absolute_import

from collections import OrderedDict
from contextlib import closing
import os
import shutil

from .config import MagicConfig, write_ini, read_ini
from .errors import InvalidOperationError
from .utils import find_executable, iter_to_list


def guess_config(known_config):
    """you can provide known config settings as

       known_config = { "db.connection_string:"...",
                        "worker.port": 3333 }

       which will overrung the settings we guess in this function
    """

    assert isinstance(known_config, dict)

    executables = ("matlab", "R", "julia", "python3")
    sections = ("matlab", "r", "julia", "python")

    messages = []

    # we use OrderedDict to guarantee stable ordering of entries in config
    # file(s)
    config = OrderedDict()
    for executable, section in zip(executables, sections):
        path = find_executable(executable, "")
        if not path:
            messages.append("{!r} not found on $PATH".format(executable))
        config["{}.executable".format(section)] = path

    config.update(known_config)

    return default_config(config), messages


def default_config(known_config):
    """you can overwrite with calls like:

        default_config(db.connections_string="....",
                       worker.port=3333)
    """

    config = MagicConfig()

    config.db.connection_string = "postgresql://user:password@127.0.0.1:5432/datapool"

    config.backup_landing_zone.folder = ""

    config.r.extension = ".r"

    config.matlab.extension = ".m"

    config.julia.extension = ".jl"
    config.julia.version = "0.5.0"

    config.python.extension = ".py"

    config.logging.config_file = "./logging_config.yaml"
    config.log_receiver.port = 5559

    config.worker.port = 5555
    config.worker.count = 5

    for key, value in known_config.items():
        fields = key.split(".")
        assert len(fields) == 2
        section, field = fields
        setattr(getattr(config, section), field, value)

    return config


def config_for_develop_db(landing_zone_folder):
    config = MagicConfig()
    path = os.path.join(landing_zone_folder, ".develop.db")
    config.connection_string = "sqlite+pysqlite:///{}".format(path)
    return config, path


def check_folder(folder):

    if not os.path.exists(folder):
        return "folder '{}' does not exist".format(folder)

    try:
        existing_files = os.listdir(folder)
    except IOError:
        return "can list content of folder '{}'".format(folder)

    existing_files = [f for f in existing_files if not f.startswith(".")]

    if existing_files:
        return "folder is not empty '{}'".format(folder)

    marker_file = os.path.join(folder, ".marker")
    try:
        open(marker_file, "w").close()
    except IOError:
        return "can not write to folder '{}'".format(folder)

    os.remove(marker_file)


@iter_to_list
def check_config(config):

    from .database import connect_to_db

    @iter_to_list
    def check(section, field, type, maybe_empty=True):
        if section not in config.keys():
            yield False, "- section {} missing".format(section)
        if field not in config[section].keys():
            yield False, "- field {} in section {} missing".format(field, section)

        value = config[section][field]
        if not maybe_empty and value == "":
            yield False, "- field {} in section {} has no value set".format(field, section)
        if not isinstance(value, type):
            yield (False, "- field {} in section {} is not of type {}".format(field, section,
                                                                              type.__name__))

    errors = check("landing_zone", "folder", str, False)
    yield from errors

    if not errors and config.landing_zone.folder:
        yield True, "- check landing zone '{}'".format(config.landing_zone.folder)
        msg = check_folder(config.landing_zone.folder)
        if msg is not None:
            yield False, "- {}".format(msg)

    errors = check("backup_landing_zone", "folder", str, True)
    yield from errors

    if not errors and config.backup_landing_zone.folder:
        yield True, "- check backup folder '{}'".format(config.backup_landing_zone.folder)
        msg = check_folder(config.backup_landing_zone.folder)
        if msg is not None:
            yield False, "- {}".format(msg)

    errors = check("db", "connection_string", str, False)
    yield from errors

    if not errors:
        try:
            yield True, "- try to connect to db"
            connect_to_db(config.db)
            yield True, "  - connected to db"
        except Exception as e:
            yield False, "  - {}".format(e)

    errors = check("r", "extension", str, False)
    yield from errors

    errors = check("r", "executable", str)
    yield from errors

    if not errors:
        if config.r.executable == "":
            yield True, "- R not configured, skip tests"
        else:
            yield True, "- check R configuration + code execution"
            from .r_runner import RRunner
            m = RRunner(config.r.executable)
            try:
                m.start_interpreter()
                yield True, "- R interpreter works"
            except:
                yield False, "  - could not start R from {}".format(config.r.executable)

    errors = check("matlab", "extension", str, False)
    yield from errors

    errors = check("matlab", "executable", str)
    yield from errors
    if not errors:
        if config.matlab.executable == "":
            yield True, "- matlab not configured, skip tests"
        else:
            yield True, "- check matlab configuration + code execution"
            from .matlab_runner import MatlabRunner
            m = MatlabRunner(config.matlab.executable)
            try:
                m.start_interpreter()
                yield True, "- matlab interpreter works"
            except:
                yield False, "  - could not start matlab from {}".format(config.matlab.executable)

    errors = check("julia", "extension", str, False)
    yield from errors

    errors = check("julia", "executable", str)
    yield from errors

    if not errors:
        if config.julia.executable == "":
            yield True, "- julia not configured, skip tests"
        else:
            yield True, "- check julia configuration + code execution"
            from .julia_runner import JuliaRunner
            m = JuliaRunner(config.julia.executable)
            try:
                m.start_interpreter()
                yield True, "- julia interpreter works"
            except:
                yield False, "  - could not start julia from {}".format(config.julia.executable)
            else:
                version = m.get_julia_version_string()
                if config.julia.version != version:
                    yield False, ("- julia interpreter is of version {}, configured is {}"
                                  "".format(version, config.julia.version))
                else:
                    yield True, "- checked julia version."

    errors = check("python", "extension", str, False)
    yield from errors

    errors = check("python", "executable", str)
    yield from errors

    if not errors:
        if config.python.executable == "":
            yield True, "- python not configured, skip tests"
        else:
            yield True, "- check python configuration + code execution"
            from .python_runner import PythonRunner
            m = PythonRunner(config.python.executable)
            try:
                m.start_interpreter()
                yield True, "- python interpreter works"
            except:
                yield False, "  - could not start python from {}".format(config.python.executable)

    errors = check("logging", "config_file", str, "")
    yield from errors

    # local import avoids circular import here:
    from .logger import resolve_logger_config_path
    if not errors and not os.path.exists(resolve_logger_config_path(config)):
        yield (False, "- configured config logging config {} does not exist".format(
            config.logging.config_file))
    yield from errors

    errors = check("log_receiver", "port", int)
    yield from errors

    if not errors:
        port = config.log_receiver.port
        if _is_port_used(port):
            yield False, "- configured log_receiver port {} is already in use".format(port)

    errors = check("worker", "port", int)
    yield from errors

    if not errors:
        port = config.worker.port
        if _is_port_used(port):
            yield False, "- configured worker port {} is already in use".format(port)

    errors = check("worker", "count", int)
    yield from errors
    if not errors and config.worker.count <= 0:
        yield (False, "- configured worker count value {} is not greater than zero".format(
            config.worker.count))


def _is_port_used(port):
    import socket
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(.5)
        return sock.connect_ex(('127.0.0.1', port)) == 0


def datapool_folder():
    etc = os.environ.get("ETC", "/etc")
    data_pool_folder = os.path.join(etc, "datapool")
    return os.path.abspath(data_pool_folder)


def datapool_ini_file_path():
    folder = datapool_folder()
    path = os.path.join(folder, "datapool.ini")
    return path


def init_config(landing_zone_folder, sqlite_db=False, overwrite=False):

    config_folder = datapool_folder()

    if os.path.exists(config_folder):
        if not overwrite:
            raise InvalidOperationError("datapool folder {} already exists".format(config_folder))
    else:
        try:
            os.makedirs(config_folder)
        except PermissionError:
            raise InvalidOperationError("creation of {} failed. try sudo.".format(config_folder))

    path = datapool_ini_file_path()

    # we use OrderedDict to guarantee stable ordering of entries in config
    # file(s)
    known_settings = OrderedDict([("landing_zone.folder", landing_zone_folder)])
    if sqlite_db:
        db_path = os.path.join(landing_zone_folder, ".simple.db")
        known_settings["db.connection_string"] = "sqlite+pysqlite:///{}".format(db_path)

    config, messages = guess_config(known_settings)

    try:
        write_ini(config, path)
    except PermissionError:
        raise InvalidOperationError("could not write {}. try sudo.".format(path))

    from .utils import abs_folder
    default_log_config = os.path.join(abs_folder(__file__), "cmdline_logging.yaml")
    shutil.copy(default_log_config, os.path.join(config_folder, config.logging.config_file))

    return config_folder, messages


def read_config(**variable_settings):
    path = datapool_ini_file_path()
    if os.path.exists(path):
        return read_ini(path, variable_settings)
    else:
        return None


def write_config(config):
    assert "__file__" in config.keys()
    write_ini(config, config.__file__)
