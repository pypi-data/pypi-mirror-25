# encoding: utf-8
from __future__ import print_function, division, absolute_import

import time
from queue import Queue

import pytest

from datapool.observer import Observer, CREATED_EVENT, ILLEGAL_EVENT


def test_call_back(tmpdir, setup_logger):

    changes = Queue()

    def call_back(event, rel_path):
        changes.put((event, rel_path))

    o = Observer(tmpdir.strpath, call_back)
    o.start()

    # create yaml file
    fh = open(tmpdir.join("site.yaml").strpath, "w")
    fh.write("x")
    fh.close()

    time.sleep(.1)

    for i in range(5):
        # create raw file "inwrite" mode, must not trigger event:
        fh = open(tmpdir.join("data.raw.inwrite").strpath, "w")
        fh.write("abc")
        fh.close()

        # should trigger a file creation event
        tmpdir.join("data.raw.inwrite").rename(tmpdir.join("data-%03d.raw" % i))

    tmpdir.join("site.yaml").remove()

    # average latency on linux is 500 msec, on mac it is faster:
    time.sleep(.7)

    o.stop()

    CE = CREATED_EVENT
    IE = ILLEGAL_EVENT
    assert sorted(changes.queue) == [(CE, 'data-000.raw'), (CE, 'data-001.raw'),
                                     (CE, 'data-002.raw'), (CE, 'data-003.raw'),
                                     (CE, 'data-004.raw'), (CE, 'site.yaml'), (IE, 'site.yaml')]


def test_exception_propagation(tmpdir, setup_logger):
    def call_back(event, rel_path):
        pass

    # we check if excdeptions are passed from background observer thread to main thread:
    o = Observer(tmpdir.join("nonexisting_subfolder").strpath, call_back)
    with pytest.raises((FileNotFoundError, OSError)):
        o.start()
