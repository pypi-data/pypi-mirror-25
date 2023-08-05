# encoding: utf-8
from __future__ import print_function, division, absolute_import

from datapool.r_runner import RRunner
from datapool.config_handling import guess_config
from datapool.utils import find_executable

import pytest

has_r = find_executable("R") is not None

# we skip this test file if matlab is not installed on the test system:
# see http://doc.pytest.org/en/latest/skipping.html#skip-all-test-functions-of-a-class-or-module
pytestmark = pytest.mark.skipif(not has_r, reason="no R interpreter found on your system")


@pytest.fixture
def r_exe(regtest):
    config, messages = guess_config({})
    assert config.r.executable != "", str(config)
    return config.r.executable


def test_r(r_exe, setup_logger):
    r = RRunner(r_exe)
    r.start_interpreter()
    assert r.is_alive()


def test_r_exception(r_exe, regtest_logger):
    with regtest_logger():
        r = RRunner(r_exe)
        r.start_interpreter()
        assert r.run_command("g <- function() { b; }; a <- g(); ") == 1
    assert r.is_alive()


def test_failed_startup(r_exe, regtest_logger):
    class FailingRRunner(RRunner):

        EXTRA_ARGS = ["--arch=XXX"]

    with regtest_logger():
        r = FailingRRunner(r_exe)
        r.start_interpreter()
