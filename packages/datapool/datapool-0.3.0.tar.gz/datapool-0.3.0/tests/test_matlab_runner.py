# encoding: utf-8
from __future__ import print_function, division, absolute_import

from datapool.matlab_runner import MatlabRunner
from datapool.utils import find_executable

import pytest

has_matlab = find_executable("matlab") is not None

# we skip this test file if matlab is not installed on the test system:
# see http://doc.pytest.org/en/latest/skipping.html#skip-all-test-functions-of-a-class-or-module
pytestmark = pytest.mark.skipif(not has_matlab, reason="no matlab interpreter found on your system")
"""
contrary to test_julia_runner we do not test the restart in case of execeeded memory consumption
or exceeded call count, the matlab startup is very slow, so we implemented an extra check for
this functionality in test_interpreter_bridge.py
"""


def test_matlab_runner(matlab_exe, regtest_logger):
    with regtest_logger():
        m = MatlabRunner(matlab_exe)
        m.start_interpreter()
        assert m.is_alive()


def test_matlab_exception(matlab_exe, regtest_logger):
    m = MatlabRunner(matlab_exe)
    m.start_interpreter()
    with regtest_logger():
        assert m.run_command("a = b;") == 1
    assert m.is_alive()
