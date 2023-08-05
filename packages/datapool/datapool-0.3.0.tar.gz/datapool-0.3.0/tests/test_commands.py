# encoding: utf-8
from __future__ import print_function, division, absolute_import

from functools import partial
import io
import os
import shutil
import threading
import time

import pytest

from datapool.utils import find_executable

from datapool.commands import (start_develop, check, check_config, update_operational, init_config,
                               init_db, run_simple_server, create_example)

from datapool.landing_zone import LandingZone

from .conftest import _fix_reg_output

has_matlab = find_executable("matlab") is not None


@pytest.yield_fixture
def m_regtest(regtest):
    """
    return regest fixture with identifier based on found / missing matlab. this identifier
    is incorporated to the file name holding the recorded output.
    so we get here different such files depending on the fact of matlab is installed or not.
    """
    if has_matlab:
        regtest.identifier = "with_matlab"
    else:
        regtest.identifier = "without_matlab"
    yield regtest
    del regtest.identifier


def _print_filtered(tmpdir, file, *args, **kw):
    """replaces tmpdir substrings from output which could change from test to test
    """
    stream = io.StringIO()
    if "fg" in kw:
        kw.pop("fg")
    print(*args, file=stream, **kw)
    content = _fix_reg_output(stream.getvalue(), tmpdir)
    file.write(content)


@pytest.fixture
def print_ok(m_regtest, tmpdir):
    """returns print_ok function which prints using m_regtest and replaces tmpdir substrings,
    adds prefix 'stdout:' to every line
    """
    return partial(_print_filtered, tmpdir, m_regtest, "stdout:")


@pytest.fixture
def print_err(m_regtest, tmpdir):
    """returns print_ok function which prints using m_regtest and replaces tmpdir substrings,
    adds prefix 'stderr:' to every line
    """
    return partial(_print_filtered, tmpdir, m_regtest, "stderr:")


def test_init_config(print_ok, print_err, tmpdir, monkeypatch, regtest_list_folders):

    monkeypatch.setenv("ETC", tmpdir.strpath)

    fresh_landing_zone = tmpdir.join("landing_zone").mkdir().strpath
    assert init_config(fresh_landing_zone, False, False, print_ok, print_err) == 0

    regtest_list_folders(fresh_landing_zone, recurse=True)

    # try new folder, should fail because the datapool config folder was created before:
    non_existing_folder = tmpdir.join("landing_zone_0").mkdir().strpath
    assert init_config(non_existing_folder, False, False, print_ok, print_err) == 1


def test_init_config_sqlite_db(print_ok, print_err, tmpdir, monkeypatch, regtest_list_folders):

    monkeypatch.setenv("ETC", tmpdir.strpath)

    fresh_landing_zone = tmpdir.join("landing_zone").mkdir().strpath
    assert init_config(fresh_landing_zone, False, True, print_ok, print_err) == 0


def test_init_db(print_ok, print_err, tmpdir, monkeypatch, regtest_list_folders):

    monkeypatch.setenv("ETC", tmpdir.strpath)
    from datapool.config_handling import read_config, write_config

    # without init_config:
    assert init_db(False, False, print_ok, print_err) == 1

    # we setup a config, but setup local db
    fresh_landing_zone = tmpdir.join("landing_zone").mkdir().strpath
    init_config(fresh_landing_zone, False, False, print_ok, print_err)
    config = read_config()
    config.db.connection_string = "sqlite+pysqlite:///{}/develop.db".format(tmpdir)
    write_config(config)

    print_ok("")
    print_ok("REGULAR INIT DB:")
    assert init_db(False, False, print_ok, print_err) == 0

    print_ok("")
    print_ok("INIT BUT DB EXISTS:")
    # db already exists
    assert init_db(False, False, print_ok, print_err) == 1

    # with reset:
    print_ok("")
    print_ok("INIT, DB EXISTS BUT WE USE RESET:")
    assert init_db(True, False, print_ok, print_err) == 0


def test_check_config(print_ok, print_err, tmpdir, monkeypatch, regtest_list_folders):
    from datapool.config_handling import read_config, write_config

    monkeypatch.setenv("ETC", tmpdir.strpath)
    assert check_config(print_ok, print_err) == 1

    fresh_landing_zone = tmpdir.join("landing_zone")
    fresh_landing_zone.mkdir()
    print_ok("init config:\n")
    init_config(fresh_landing_zone.strpath, False, False, print_ok, print_err)

    print_ok("\ncheck config:\n")
    assert check_config(print_ok, print_err) == 1

    config = read_config()
    config.julia.version = "0.0.0"
    write_config(config)
    print_ok("\ncheck config:\n")
    assert check_config(print_ok, print_err) == 1


def test_start_develop(print_ok, print_err, tmpdir, monkeypatch, regtest_list_folders):
    from datapool.config_handling import read_config, write_config

    monkeypatch.setenv("ETC", tmpdir.strpath)

    operational_landing_zone = tmpdir.join("landing_zone").mkdir()

    print_ok("init config:\n")
    init_config(operational_landing_zone.strpath, False, False, print_ok, print_err)

    llz = tmpdir.join("local_landing_zone")

    sd = partial(start_develop, verbose=False, print_ok=print_ok, print_err=print_err)

    print_ok("\nstart develop:\n")
    sd(llz.strpath, reset=False)

    regtest_list_folders(llz.strpath, recurse=True)

    # overwrite existing landing zone, reset = True
    print_ok("\nstart develop:\n")
    sd(llz.strpath, reset=True)

    regtest_list_folders(llz.strpath, recurse=True)

    # error case: try to overwrite existing landing zone, reset = False
    print_ok("\nstart develop:\n")

    sd(llz.strpath, reset=False)

    # wrong access rights for reset of existing landing zone:
    print_ok("\nstart develop:\n")
    llz.chmod(0o444)
    sd(llz.strpath, reset=True)
    llz.chmod(0o777)

    # wrong access rights for copying landing zone:
    operational_landing_zone.chmod(0o000)
    assert sd(llz.strpath, reset=True) == 1
    operational_landing_zone.chmod(0o777)

    # fresh landing zone but develop db already holds the tables:
    config = read_config()
    config.db.connection_string = "sqlite+pysqlite:///{}/fake_master.db".format(tmpdir)
    write_config(config)
    assert init_db(False, False, print_ok, print_err) == 0

    # inject invalid operational landing zone
    config.landing_zone.folder += "x"
    write_config(config)
    assert sd(llz.strpath, reset=True) == 1


def test_update_operational(print_ok, print_err, tmpdir, monkeypatch, regtest):

    monkeypatch.setenv("ETC", tmpdir.strpath)

    operational_landing_zone = tmpdir.join("landing_zone").mkdir()
    llz = tmpdir.join("local_landing_zone")

    sd = partial(start_develop, verbose=False, print_ok=print_ok, print_err=print_err)
    uo = partial(update_operational, verbose=True, print_ok=print_ok, print_err=print_err)

    init_config(operational_landing_zone.strpath, True, True, print_ok, print_err)
    init_db(reset=True, verbose=False, print_ok=print_ok, print_err=print_err)

    assert sd(llz.strpath, reset=False) == 0

    print_ok("")
    print_ok("regular update_operational".upper())
    if uo(llz.strpath, overwrite=False) != 0:
        return

    print_ok("")
    print_ok("update_operational zero updates:".upper())
    uo(llz.strpath, overwrite=False)


def test_check(print_ok, print_err, tmpdir, monkeypatch, data_path):

    monkeypatch.setenv("ETC", tmpdir.strpath)

    operational_landing_zone = tmpdir.join("landing_zone").mkdir()

    print_ok("init config:\n")
    init_config(operational_landing_zone.strpath, sqlite_db=True, reset=True, print_ok=print_ok,
                print_err=print_err)

    init_db(reset=True, verbose=False, print_ok=print_ok, print_err=print_err)

    llz = tmpdir.join("local_landing_zone")

    ce = partial(create_example, print_ok=print_ok, print_err=print_err)

    print_ok("")
    print_ok("START DEVELOP")
    assert ce(llz.strpath, reset=False) == 0

    # ok
    print_ok("")
    print_ok("CHECK OK EXCEPT MAYBE MATLAB")
    check(llz.strpath, None, False, print_ok, print_err)

    shutil.copy(data_path("yamls/modified_site.yaml"),
                llz.join("sites/example_site/site.yaml").strpath)
    print_ok("")
    print_ok("YAML CHECK STILL OK")
    check(llz.strpath, None, False, print_ok, print_err)

    # multiple signals
    raw_folder = llz.join("data/sensor_from_company_xyz/sensor_instance_python/raw_data")
    shutil.copy(raw_folder.join("data-001.raw").strpath, raw_folder.join("data-002.raw").strpath)
    print_ok("")
    print_ok("FAILS BECAUSE DUPLICATE SIGNALS")
    check(llz.strpath, None, False, print_ok, print_err)

    # cleanup
    os.remove(raw_folder.join("data-002.raw").strpath)

    # invalid path
    print_ok("")
    print_ok("CHECK NONEXISTING FOLDER")
    check("/tmp/def/this_folder_will_not_exist/42", None, True, print_ok, print_err)

    lz = LandingZone(llz.strpath)
    lz.overwrite_file("data/sensor_from_company_xyz/sensor_instance_julia/conversion.jl",
                      data_path("failing_scripts", "conversion_exceeds_dimensions.jl"))

    print_ok("")
    print_ok("CHECK JULIA FAILS")
    check(llz.strpath, None, False, print_ok, print_err)

    lz.overwrite_file("sites/example_site/site.yaml", data_path("yamls/empty.yaml"))
    lz.overwrite_file("sites/example_site/site.yaml",
                      data_path("yamls/site_with_invalid_pictures.yaml"))
    # ok
    print_ok("")
    print_ok("CHECK YAMLS FAILD")
    check(llz.strpath, None, False, print_ok, print_err)


def test_run_simple_server(print_ok, print_err, monkeypatch, tmpdir, lz, data_path):
    from datapool.config_handling import (init_config, read_config, write_config,
                                          config_for_develop_db)

    monkeypatch.setenv("ETC", tmpdir.strpath)

    config_folder, messages = init_config(lz.root_folder, overwrite=True, sqlite_db=False)
    config = read_config()
    config.db, __ = config_for_develop_db(lz.root_folder)
    write_config(config)

    started = time.time()

    def run_for_n_seconds():
        return time.time() < started + 1.8

    def inject_change():
        time.sleep(.8)
        lz.overwrite_file("test.yaml", data_path("yamls/empty.yaml"))
        time.sleep(.2)
        lz.overwrite_file("sites/example_site/site.yaml", data_path("yamls/empty.yaml"))
        time.sleep(.2)
        lz.overwrite_file("data/parameters.yaml", data_path("yamls/parameters_extended.yaml"))

    threading.Thread(target=inject_change).start()
    run_simple_server(False, print_ok, print_err, run_for_n_seconds)


def test_development_workflow(print_ok, print_err, tmpdir, monkeypatch, data_path, regtest):

    monkeypatch.setenv("ETC", tmpdir.strpath)

    operational_landing_zone = tmpdir.join("landing_zone").mkdir().strpath
    development_landing_zone = tmpdir.join("development_landing_zone").strpath

    steps = [
        partial(init_config, operational_landing_zone, True, True, print_ok, print_err),
        partial(check_config, print_ok, print_err),
        partial(init_db, True, False, print_ok, print_err),
        partial(create_example, development_landing_zone, False, print_ok, print_err),
        partial(check, development_landing_zone, None, False, print_ok, print_err),
        partial(update_operational, development_landing_zone, False, False, print_ok, print_err),
    ]

    expected_rcs = [0, 0, 0, 0, None]

    for step, expected_rc in zip(steps, expected_rcs):
        func_name = step.func.__name__
        print(file=regtest)
        print("run", func_name, file=regtest)
        rc = step()
        if expected_rc is not None and rc != expected_rc:
            print(file=regtest)
            print("=" * 100, file=regtest)
            print("{} returned {}".format(func_name, rc), file=regtest)
            print("=" * 100, file=regtest)
            print(file=regtest)
            break
