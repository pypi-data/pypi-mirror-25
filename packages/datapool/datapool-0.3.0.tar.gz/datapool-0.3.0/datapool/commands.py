from __future__ import print_function, division, absolute_import

from os.path import join, exists

import contextlib
import os
import queue
import shutil
import signal
import tempfile
import time

from .config_handling import config_for_develop_db, read_config
from .data_conversion import ConversionRunner
from .database import connect_to_db, setup_db, setup_fresh_db, check_if_tables_exist, copy_db
from .dispatcher import Dispatcher
from .domain_objects_checker import DomainObjectsChecker
from .errors import InvalidOperationError, InvalidLandingZone, DataPoolException
from .landing_zone import LandingZone, write_lock
from .landing_zone_structure import lock_file, source_yaml_path_for_script
from .logger import setup_logger_from, drop_logger, check_logging_config, logger
from .observer import start_observer, shutdown_observer, CREATED_EVENT, MODIFIED_EVENT
from .signal_model import check_signals_against_db, check_fields, check_signals_uniqueness
from .uniform_file_format import to_signals
from .utils import abs_folder, enumerate_filename, print_signals
from .yaml_parsers import parse_source


@contextlib.contextmanager
def get_cmdline_logger(verbose):
    config_file = join(abs_folder(__file__), "cmdline_logging.yaml")
    drop_logger()
    setup_logger_from(config_file)
    if verbose:
        logger().setLevel(10)
    yield
    drop_logger()


def init_config(landing_zone, sqlite_db, reset, print_ok, print_err, verbose=False):
    """setup minimal landing zone and create default configuration """

    from .config_handling import init_config
    with get_cmdline_logger(verbose):

        if not exists(landing_zone):
            print_err("+ folder {} does not exist".format(landing_zone))
            return 1
        print_ok("- guess settings")
        try:
            landing_zone = os.path.abspath(landing_zone)
            config_folder, messages = init_config(landing_zone, sqlite_db, overwrite=reset)
            for message in messages:
                print_err("  - {}".format(message))
            print_ok("- created config files at {}".format(config_folder))
            print_ok(
                "  please edit these files and adapt the data base configuration to your setup")
        except Exception as e:
            print_err("+ something went wrong: {}".format(e))
            return 1

        return 0


def check_config(print_ok, print_err, verbose=False):
    """checks if current configuration is valid, eg if database access is possible, or
    if matlab can be started.
    """
    from .config_handling import check_config

    config = read_config()
    if config is None:
        print_err("- no config file found. please run 'pool init-config' first.")
        return 1

    if config is None:
        print_err("- no config file found. please run 'pool init-config' first.")
        return 1

    print_ok("- check settings in config file {}".format(config.__file__))
    try:
        check_logging_config(config)
    except Exception as e:
        print_err("- could not setup logger. hint: {}".format(e))
        return 1

    with get_cmdline_logger(verbose):
        overall_ok = True
        for ok, message in check_config(config):
            if ok:
                print_ok(message)
            else:
                print_err(message)
                overall_ok = False
    if overall_ok:
        print_ok("+ all checks passed", fg="green")
    else:
        print_err("+ at least on check failed")
    return 0 if overall_ok else 1


def init_db(reset, verbose, print_ok, print_err):
    """creates empty tables in configured database, can be used to delete data from an existing
    database.
    """

    with get_cmdline_logger(verbose):

        config = read_config()
        if config is None:
            print_err("+ no config file found. please run 'pool init' first.")
            return 1

        try:
            already_exists = check_if_tables_exist(config.db)
        except InvalidOperationError as e:
            print_err("+ can not check database: {}".format(e))
            return 1
        if already_exists:
            if reset:
                setup_fresh_db(config.db, verbose=verbose)
            else:
                print_err("+ database is already initialized, use --force TWICE to setup a fresh "
                          "and empty database. YOU WILL LOOSE ALL EXISTING DATA !!!")
                return 1
        else:
            setup_db(config.db, verbose=verbose)

        print_ok("+ intialized db", fg="green")
        return 0


def _setup_landing_zone(development_landing_zone, operational_landing_zone, is_first_time, reset,
                        print_ok, print_err):

    print_ok("- setup development landing zone")
    if exists(development_landing_zone):
        if not reset:
            print_err("  - folder {} already exists.".format(development_landing_zone))
            return 1
        else:
            try:
                shutil.rmtree(development_landing_zone)
            except Exception as e:
                print_err("  - could not delete folder {}".format(development_landing_zone))
                print_err("  - error message is: {}".format(e))
                return 1

    try:
        if is_first_time:
            print_ok("- operational landing zone is empty. you might use 'pool create-example' "
                     "to see how to setup an initial landing zone.")
            LandingZone.create_empty(development_landing_zone)
        else:
            print_ok("- copy files from operational landing zone.")
            LandingZone.create_from(development_landing_zone, operational_landing_zone)
    except IOError as e:
        print_err("- something went wrong: {}".format(e))
        return 1
    return 0


def create_example(development_landing_zone, reset, print_ok, print_err):
    """creates local example landing zone serving examples for the initial setup.
    """

    print_ok("- setup example landing zone")

    if exists(development_landing_zone):
        if not reset:
            print_err("  - folder {} already exists.".format(development_landing_zone))
            return 1
        else:
            try:
                shutil.rmtree(development_landing_zone)
            except Exception as e:
                print_err("  - could not delete folder {}".format(development_landing_zone))
                print_err("  - error message is: {}".format(e))
                return 1

    LandingZone.create_from_empty(development_landing_zone)

    print_ok("+ example landing zone created", fg="green")
    return 0


def start_develop(development_landing_zone, reset, verbose, print_ok, print_err):
    """creates local landing zone for integrating new devices, conversion scripts etc.
    either the configured operational landing zone is cloned or example files are written to
    the local landing zone.
    Further a local sqlite database is created.

    if "reset" is True existing folders and database will be overwritten.
    """

    config = read_config(DEVELOPZONE=development_landing_zone)
    if config is None:
        print_err("- no config file found. please run 'pool init-config' first.")
        return 1

    operational_landing_zone = config.landing_zone.folder

    if not exists(operational_landing_zone):
        print_err("+ configured landing zone {} does not exist".format(operational_landing_zone))
        return 1

    try:
        files = os.listdir(operational_landing_zone)
        files = [f for f in files if not f.startswith(".")]
        is_first_time = (files == [])
    except IOError as e:
        print_err("+ can not read {}: {}".format(operational_landing_zone, e))
        return 1

    with get_cmdline_logger(verbose):
        exit_code = _setup_landing_zone(development_landing_zone, operational_landing_zone,
                                        is_first_time, reset, print_ok, print_err)

    if exit_code:
        print_err("+ setup failed")
    else:
        print_ok("+ setup done", fg="green")
    return exit_code


def _setup(print_err, landing_zone, **kw):

    config = read_config(**kw)
    if config is None:
        print_err("- no config file found. please run 'pool init-config' first.")
        return None, None

    if not exists(landing_zone):
        print_err("  - folder {} does not exist".format(landing_zone))
        return None, None
    try:
        lz = LandingZone(landing_zone)
    except InvalidLandingZone as e:
        print_err("  - landing zone at {} invalid. reason: {}".format(landing_zone, e))
        return None, None
    return config, lz


def check(landing_zone, result_folder, verbose, print_ok, print_err, run_twice=True):

    config, lz = _setup(print_err, landing_zone)
    if config is None or lz is None:
        return 1

    print_ok("- check names and places of changed files at landing zone {}".format(landing_zone))
    all_changed_files = set(lz.list_new_and_changed_files())
    __, unknown_files = lz.separate_allowed_files(all_changed_files)

    if not unknown_files:
        print_ok("- file names and their places are ok")
    else:
        for unknown_file in unknown_files:
            print_err("- do not know how to handle file at {}".format(unknown_file))

    print_ok("- check yaml files in landing zone at {}".format(landing_zone))

    with get_cmdline_logger(verbose):
        with _setup_test_db(landing_zone, config, verbose, print_ok, print_err) as engine:

            ok = _run_yaml_checks(lz, engine, print_ok, print_err, verbose)
            if not ok:
                print_err("+ detected problems in yaml files")
                return 1
            print_ok("- all yaml files checked")

            print_ok("- check scripts landing zone at {}".format(landing_zone))
            found_errors = _run_script_checks(lz, engine, config, result_folder, verbose, run_twice,
                                              print_ok, print_err)

    if found_errors:
        print_err("+ checks failed. please fix this.")
        return 1

    print_ok("- all scripts checked")
    print_ok("+ congratulations: all checks succeeded.", fg="green")
    return 0


def _run_script_checks(lz, engine, config, result_folder, verbose, run_twice, print_ok, print_err):

    runner = ConversionRunner(config)
    result_folder = _setup_result_folder(result_folder, print_ok, print_err)

    found_errors = False
    changed_files = lz.list_new_and_changed_files()

    all_signals = []

    for script_path, data_path in lz.conversion_scripts_and_data():

        if script_path not in changed_files and data_path not in changed_files:
            print_ok("- skip conversion of {} by {}. both are unchanged"
                     .format(data_path, script_path))
            continue

        print_ok("- check {} on {}".format(script_path, data_path))

        source = _load_source(lz, script_path, print_err)
        if source is None:
            found_errors = True
            continue

        ok, needed_conv, signals = _check_conversion(runner, lz, script_path, data_path, verbose,
                                                     result_folder, source, True,
                                                     print_ok, print_err)
        if signals is not None:
            all_signals.extend(signals)

        if not ok:
            found_errors = True
        else:
            print_ok("  - first conversion needed {:.0f} msec".format(needed_conv * 1000))
            if run_twice:
                ok, needed_conv, __ = _check_conversion(runner, lz, script_path, data_path,
                                                        verbose, result_folder, source, False,
                                                        print_ok, print_err)
                if not ok:
                    found_errors = True
                else:
                    print_ok("  - second conversion needed {:.0f} msec".format(needed_conv * 1000))

    if found_errors:
        return True

    print_ok("- check signals integrity")
    found_errors = _report(check_signals_uniqueness(all_signals), print_err)
    if not found_errors:
        print_ok("- check signals against db")
        found_errors = _report(check_signals_against_db(all_signals, engine), print_err)
    return found_errors


def _load_source(lz, script_path, print_err):
    source_path = source_yaml_path_for_script(script_path)

    source = None
    for result in parse_source(lz.root_folder, source_path):
        if isinstance(result, DataPoolException):
            print_err("  - parsing {}: {}".format(source_path, result))
        else:
            source = result

    return source


def _check_conversion(runner, lz, script_path, data_path, verbose, result_folder, source,
                      backup_results, print_ok, print_err):

    signals = None

    started = time.time()
    for result in runner.check_conversion(lz.p(script_path), lz.p(data_path), verbose):
        if isinstance(result, Exception):
            print_err("  - {}".format(result))
        else:
            output_file, rows = result
            signals = to_signals(rows)

    if signals is None:
        return False, 0, signals

    needed_conv = time.time() - started

    for signal in signals:
        signal.source = source.name

    if backup_results:
        _backup_results(result_folder, output_file, signals, script_path, print_ok)

    has_errors = _report(check_fields(signals), print_err)
    return not has_errors, needed_conv, signals


def _report(check_iter, print_err):
    error_count = 0
    has_errors = False
    errors = list(check_iter)
    MAX_ERR = 10
    for exc in errors:
        print_err("  - {}".format(exc))
        error_count += 1
        has_errors = True
        if error_count > MAX_ERR:
            print_err("  - too many errors, skipped {} errors.".format(len(errors) - MAX_ERR))
            break
    return has_errors


def _setup_result_folder(result_folder, print_ok, print_err):

    if not result_folder:
        result_folder = tempfile.mkdtemp()
    else:
        if os.path.exists(result_folder):
            if not os.path.isdir(result_folder):
                print_err("+ given path {} exists but is not a folder".format(result_folder))
                return 1
        else:
            os.makedirs(result_folder)
            print_ok("- created folder {}".format(result_folder))

    return result_folder


def _backup_results(result_folder, output_file, signals, script, print_ok):
    script_folder_name = os.path.basename(os.path.dirname(script))
    csv_path = join(result_folder, script_folder_name) + ".csv"
    txt_path = join(result_folder, script_folder_name) + ".txt"

    csv_path, txt_path = enumerate_filename(csv_path, txt_path)
    shutil.copy(output_file, csv_path)
    print_ok("  - wrote conversion result as csv to {}".format(csv_path))
    with open(txt_path, "w") as fh:
        print_signals(signals, file=fh)
    print_ok("  - wrote conversion result as txt to {}".format(txt_path))


def update_operational(development_landing_zone, verbose, overwrite, print_ok, print_err):

    config = read_config()
    if config is None:
        print_err("- no config file found. please run 'pool init-config' first.")
        return 1

    operational_landing_zone = config.landing_zone.folder

    lz = LandingZone(development_landing_zone)
    try:
        messages = lz.check_before_update_operational(operational_landing_zone)
    except InvalidLandingZone as e:
        print_err("  - {}".format(e))

    if messages:
        for message in messages:
            print_err("  - problem: {}".format(message))
            print_ok ("  - will ignore these and overwrite existing files")
    else:
        print_ok("- development landing zone seems to be sane.")

    with write_lock(operational_landing_zone) as got_lock:

        if not got_lock:
            print_err("+ {} is locked. maybe somebody else wants to update simultaneously"
                      .format(operational_landing_zone))
            return 1

        exit_code = check(development_landing_zone, None, verbose, print_ok, print_err, False)
        if exit_code != 0:
            print_err("+ checks failed. don't copy files to {}".format(operational_landing_zone))
            return 1

        files = lz.update_operational(operational_landing_zone, delay=0.5)
        for file in files:
            print_ok("- copied {}".format(file))
        print_ok("+ copied {} files to {}".format(len(files), operational_landing_zone), fg="green")
        return 0


@contextlib.contextmanager
def _setup_test_db(landing_zone, config, verbose, print_ok, print_err):

    config_develop_db, path = config_for_develop_db(landing_zone)

    if os.path.exists(path):
        os.unlink(path)

    ok = False
    try:
        ok = check_if_tables_exist(config.db)
    except InvalidOperationError:
        print_err("- could not connect to productive db.")
    if not ok:
        print_err("- setup fresh development db. productive does not exist or is empty.")
        setup_db(config_develop_db, verbose=verbose)

    else:
        print_ok("- copy meta data from productive db")
        for table_name in copy_db(
                config.db, config_develop_db, delete_existing=True, copy_signals=False,
                verbose=verbose):
            print_ok("  - copy table {}".format(table_name))

    engine = connect_to_db(config_develop_db)

    yield engine

    os.unlink(path)
    engine.dispose()


def _run_yaml_checks(lz, engine, print_ok, print_err, verbose):

    new_yamls = []
    for rel_path in lz.list_all_files():
        if not rel_path.endswith(".yaml"):
            continue
        new_yamls.append(rel_path)

    if not new_yamls:
        print_ok("- no updates detected. skip checks.")
        return True

    print_ok("- detected {} new or modified yaml files:".format(len(new_yamls)))
    for rel_path in new_yamls:
        print_ok("  - {}".format(join(lz.root_folder, rel_path)))

    print_ok("- check yaml files")
    checker = DomainObjectsChecker(lz.root_folder, new_yamls)
    ok = True
    for error in checker.check_all(engine):
        print_err("  - got error: {}".format(error))
        ok = False

    return ok


def run_simple_server(verbose, print_ok, print_err, still_running=None):

    config = read_config()
    if config is None:
        print_err("- no config file found. please run 'pool init-config' first.")
        return 1

    with get_cmdline_logger(verbose):

        try:
            already_setup = check_if_tables_exist(config.db)
        except InvalidOperationError as e:
            print_err("+ can not check database: {}".format(e))
            return 1
        if not already_setup:
            print_ok("- setup fresh db")
            try:
                setup_db(config.db, verbose=verbose)
            except InvalidOperationError as e:
                print_err("+ can not setup database: {}".format(e))
                return 1
        else:
            print_ok("- db already setup")

        if config.julia.executable:

            print_ok("- check startup julia")
            from datapool.julia_runner import JuliaRunner
            r = JuliaRunner(config.julia.executable)
            r.start_interpreter()
            ok = r.is_alive()
            if not ok:
                 print_err("+ julia startup failed")
                 return 1

        setup = _setup_simple_server(config, print_ok, print_err, still_running)
        if setup is None:
            return 1
        print_ok("- observe {} now".format(config.landing_zone.folder))
        _simple_server_loop(still_running, setup, print_ok, print_err)

    print_ok("+ done", fg="green")

    return 0


def _setup_simple_server(config, print_ok, print_err, still_running):

    dispatcher = Dispatcher(config)
    q = queue.Queue()
    root_folder = config.landing_zone.folder

    def call_back(event, rel_path):
        if event not in (CREATED_EVENT, MODIFIED_EVENT):
            if rel_path == lock_file:
                print_ok("- removed update lock for landing zone")
            else:
                if not os.path.basename(rel_path).startswith("."):
                    print_err("- invalid event for {}".format(rel_path))
        else:
            if rel_path == lock_file:
                print_ok("- lock landing zone for updating")
            else:
                q.put((event, rel_path))

    try:
        observer = start_observer(root_folder, call_back)
    except Exception as e:
        print_err("- could not start observer: {}".format(e))
        return None

    return q, dispatcher, observer


def _simple_server_loop(still_running, setup, print_ok, print_err):

    q, dispatcher, observer = setup

    def shutdown(signum=None, frame=None):
        nonlocal old_handler
        nonlocal still_running
        print()
        if signum is not None:
            print_ok("- shutdown observer due to signal {}".format(signum))
        else:
            print_ok("- shutdown observer")
        shutdown_observer(observer)
        if signum is not None and callable(old_handler):
            old_handler(signum, frame)
        still_running = lambda: False

    old_handler = signal.signal(signal.SIGTERM, shutdown)

    try:
        while still_running is None or still_running():
            try:
                event, rel_path = q.get(timeout=.01)
            except queue.Empty:
                continue

            # we ignore dot files:
            if os.path.basename(rel_path).startswith("."):
                continue

            print_ok("- dispatch {}".format(rel_path))
            results = dispatcher.dispatch(rel_path)
            for result in results:
                if isinstance(result, str):
                    print_ok("  {}".format(result))
                else:
                    print_err("  error: {}".format(result))
            print_ok("  dispatch done")

    except KeyboardInterrupt:
        shutdown()
