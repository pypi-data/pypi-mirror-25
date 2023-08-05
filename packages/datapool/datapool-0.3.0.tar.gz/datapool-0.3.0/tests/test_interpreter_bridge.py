# encoding: utf-8
from __future__ import print_function, division, absolute_import

import functools

from datapool.interpreter_bridge import InterpreterBridge
from datapool.utils import find_executable

import pytest


@pytest.fixture
def bash_bridge():
    class BashBridge(InterpreterBridge):

        NAME = "BASH"
        MSG_MARKER = "!!!"
        TEMPLATE = """
        {command}
        echo "{MSG_MARKER}EXITCODE:0"
        echo "{MSG_MARKER}FINISHED"
        """

    bash_exe = find_executable("bash")
    return functools.partial(BashBridge, executable=bash_exe, noop="echo 0;")


def test_shell_bridge(bash_bridge, setup_logger):

    bash = bash_bridge()
    bash.start_interpreter(verbose=True)
    assert bash.is_alive()


def test_with_call_limit_exceeded(bash_bridge, setup_logger):

    j = bash_bridge(call_limit=1)
    j.start_interpreter()

    pid_before = j.pid
    j.run_command("echo 1;")
    assert j.pid == pid_before

    j.run_command("echo 2;")
    assert j.pid != pid_before


def test_with_mem_limit_exceeded(bash_bridge, setup_logger):
    j = bash_bridge(call_limit=1)
    j.start_interpreter()

    import datapool.interpreter_bridge

    injected_mem_usage = 100

    def patched_used_memory(p):
        return injected_mem_usage

    datapool.interpreter_bridge.used_memory = patched_used_memory

    j = bash_bridge(mem_limit=110)
    j.start_interpreter()

    pid_before = j.pid
    j.run_command("echo 1;")
    assert j.pid == pid_before

    injected_mem_usage = 120
    j.run_command("echo 2;")
    assert j.pid != pid_before
