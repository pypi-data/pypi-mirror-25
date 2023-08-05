# encoding: utf-8
from __future__ import print_function, division, absolute_import

import os

from datapool.config import MagicConfig, write_ini, read_ini


def test_config(regtest):

    data = MagicConfig()
    data.a = 1
    data.b.c = "2"
    data.b.d = 3.45

    assert data.a == 1
    assert data.b.c == "2"
    assert data.b["d"] == 3.45

    assert data["a"] == 1
    assert data["b"].c == "2"
    assert data["b"]["c"] == "2"
    assert data["b"].d == 3.45
    assert data["b"]["d"] == 3.45
    data.print_(fh=regtest)
    print(data, file=regtest)


def test_config_io(tmpdir):

    data = MagicConfig()

    data.workers.queue_port = 5555
    data.workers.logger_port = 5556
    data.workers.workers_port = 5557
    data.logging.console_level = "debug"
    data.logging.file_level = "debug"
    data.logging.file_path = "~/datapool/log.txt"

    path = tmpdir.join("config.ini").strpath
    write_ini(data, path)

    data_back = read_ini(path)

    assert data_back.__file__ == path
    del data_back["__file__"]  # else next test fails
    del data["__file__"]  # else next test fails

    # test roundtrip:
    assert data == data_back


def test_config_variable_resolution(tmpdir, regtest):

    data = MagicConfig()
    data.test.tmp = "$TMP"
    data.test.home = "$HOME"

    path = tmpdir.join("config.ini").strpath
    write_ini(data, path)
    print(open(path).read(), file=regtest)

    data_back = read_ini(path)
    assert "$" not in data_back.test.tmp
    assert data_back.test.home == os.environ.get("HOME")
