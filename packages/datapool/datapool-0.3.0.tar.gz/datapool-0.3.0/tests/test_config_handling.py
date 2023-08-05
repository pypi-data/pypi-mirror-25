# encoding: utf-8
from __future__ import print_function, division, absolute_import

import os

from datapool.config import read_ini, write_ini
from datapool.config_handling import (init_config, datapool_ini_file_path, check_config,
                                      check_folder)


def _check_and_cleanup_config_for_regtest(config):

    assert len(config.db.connection_string) > 0
    config.db.connection_string = "<dummy for regression tests>"

    if "landing_zone" in config:
        assert config.landing_zone.folder != ""
        config.landing_zone.folder = "<dummy for regression tests>"
    if "backup_landing_zone" in config:
        if config.backup_landing_zone.folder != "":
            config.backup_landing_zone.folder = "<dummy for regression tests>"

    config.r.executable = " <dummy for regression tests>"
    config.matlab.executable = " <dummy for regression tests>"
    config.julia.executable = " <dummy for regression tests>"


def test_faked_config(regtest, here):
    path = datapool_ini_file_path()

    # relpath to avoid absolute pathes in regtest output:
    print(os.path.relpath(path, here), file=regtest)
    config = read_ini(path)

    _check_and_cleanup_config_for_regtest(config)

    write_ini(config, regtest)


def test_init_config(monkeypatch, tmpdir, regtest, data_path, has_matlab, has_julia, has_r):

    # we patch, else we could overwrite something, eg the files in
    # ./home/datapool which is our faked home folder for testing:
    monkeypatch.setenv("ETC", tmpdir.strpath)

    folder, messages = init_config(data_path("test_landing_zone"))
    assert folder is not None
    print(sorted(os.listdir(tmpdir.strpath)), file=regtest)

    config = read_ini(datapool_ini_file_path())

    if has_matlab:
        assert not any("matlab" in message for message in messages)
        assert config.matlab.executable != "", str(config)
    else:
        assert any("matlab" in message for message in messages)
        assert config.matlab.executable == "", str(config)

    if has_julia:
        assert not any("julia" in message for message in messages)
        assert config.julia.executable != "", str(config)
    else:
        assert any("julia" in message for message in messages)
        assert config.julia.executable == "", str(config)

    if has_r:
        assert not any("r" in message for message in messages)
        assert config.r.executable != "", str(config)
    else:
        assert any("r" in message for message in messages)
        assert config.r.executable == "", str(config)

    assert config.python.executable != ""
    del config.python.executable

    _check_and_cleanup_config_for_regtest(config)

    write_ini(config, regtest)


def test_check_config(config, regtest, tmpdir, regtest_logger):

    os.makedirs(config.landing_zone.folder)
    with regtest_logger():
        messages = check_config(config)

    for message in messages:
        print(message, file=regtest)

    # we now corrupt the config
    config.worker.port = 22  # should be in use
    config.log_receiver.port = 22.23  # should be int
    config.db.connection_string = ""  # must be set
    config.r.extension = ""  # must be set
    config.r.executable = 0  # wrong type
    config.matlab.extension = ""  # must be set
    config.matlab.executable = 0  # wrong type
    config.julia.extension = ""  # must be set
    config.julia.executable = 0  # wrong type
    config.logging.config_file = "./non_existing.yaml"

    with regtest_logger():
        messages = check_config(config)

    for message in messages:
        print(message, file=regtest)


def test_check_folder(tmpdir, regtest):

    def check(folder):
        folder = folder.strpath
        result = check_folder(folder)
        if result is None:
            result = "ok"
        print("check {}: {}".format(folder, result), file=regtest)

    fldr = tmpdir.join("fresh_empty_writable_folder").mkdir()
    check(fldr)

    # not readable:
    fldr.chmod(0)
    check(fldr)

    # +rx, so not writable:
    fldr.chmod(0o555)
    check(fldr)

    # +wx, folder not empty
    fldr.chmod(0o777)
    fldr.join("file").open("w").close()
    check(fldr)
