# encoding: utf-8
from __future__ import print_function, division, absolute_import

from datapool.python_runner import PythonRunner
from datapool.config_handling import guess_config
from datapool.utils import find_executable

import pytest

has_python = find_executable("python") is not None

# we skip this test file if matlab is not installed on the test system:
# see http://doc.pytest.org/en/latest/skipping.html#skip-all-test-functions-of-a-class-or-module
pytestmark = pytest.mark.skipif(not has_python, reason="no python interpreter found on your system")


@pytest.fixture
def python_exe(regtest):
    config, messages = guess_config({})
    assert config.python.executable != "", str(config)
    return config.python.executable


def test_python(python_exe, setup_logger):
    r = PythonRunner(python_exe)
    r.start_interpreter()
    assert r.is_alive()


def test_python_exception(python_exe, regtest_logger):
    r = PythonRunner(python_exe)
    r.start_interpreter()
    with regtest_logger():
        assert r.run_command("1/0") == 1
    assert r.is_alive()
