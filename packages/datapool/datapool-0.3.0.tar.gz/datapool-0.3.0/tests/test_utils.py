# encoding: utf-8
from __future__ import print_function, division, absolute_import

import os

from datapool.utils import list_folder_recursive, enumerate_filename


def test_folder_list(data_path, regtest):
    for path in list_folder_recursive(data_path("../etc")):
        print(path, file=regtest)


def test_enumerate_filename(tmpdir):
    fldr = tmpdir.strpath
    fname = tmpdir.join("abc").strpath

    def ef(p):
        return enumerate_filename(p)[0]

    assert ef(fname) == os.path.join(fldr, "abc_0")
    assert ef(fname) == os.path.join(fldr, "abc_0")

    fname = tmpdir.join("abc.txt").strpath
    assert ef(fname) == os.path.join(fldr, "abc_0.txt")
    next_name = ef(fname)
    assert next_name == os.path.join(fldr, "abc_0.txt")

    def touch(path):
        open(path, "w").close()
        return path

    touch(fname)
    touch(next_name)
    next_name = ef(fname)
    assert next_name == os.path.join(fldr, "abc_1.txt")

    touch(next_name)
    next_name = ef(fname)
    assert next_name == os.path.join(fldr, "abc_2.txt")

    touch(os.path.join(fldr, "abc_9.txt"))
    next_name = ef(fname)
    assert next_name == os.path.join(fldr, "abc_10.txt")

    fname_1 = touch(os.path.join(fldr, "xyz.txt"))
    fname_2 = touch(os.path.join(fldr, "uvw_3.txt"))

    next_1, next_2 = enumerate_filename(fname_1, fname_2)
    assert next_1 == os.path.join(fldr, "xyz_4.txt")
    assert next_2 == os.path.join(fldr, "uvw_4.txt")
