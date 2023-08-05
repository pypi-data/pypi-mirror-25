# encoding: utf-8
from __future__ import print_function, division, absolute_import

import pytest


def test_0():
    from datapool.bunch import Bunch

    x = Bunch({"a": 3, "b": {"c": 4, "d": 5}})

    # we read
    assert x.a == 3
    assert x.b.c == 4
    assert x.b.d == 5

    # we detect access errors
    with pytest.raises(KeyError):
        x.c

    # we write
    x.c = 7
    assert x.c == 7

    # we remove
    del x.a

    # we detect access errors
    with pytest.raises(KeyError):
        x.a


def test_1():
    from datapool.bunch import Bunch

    x = Bunch({
        "a": (3, {
            "d": 7
        }),
        "b": [{
            "c": 5
        }],
    })

    assert x.b[0].c == 5
    assert x.a[1].d == 7


def test_str(regtest):
    from datapool.bunch import Bunch

    # check that str presentation is always ordered and the same:
    for i in range(10):
        dd = {}
        for key in "bcdefghijk":
            dd[key] = ord(key)
        b = Bunch(dd)
        print(b, file=regtest)
