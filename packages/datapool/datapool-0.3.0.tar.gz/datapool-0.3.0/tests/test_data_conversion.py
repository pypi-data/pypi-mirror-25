# encoding: utf-8
from __future__ import print_function, division, absolute_import

from collections import defaultdict
import os

import pytest

from datapool.data_conversion import ConversionRunner
from datapool.errors import InvalidOperationError, FormatError
from datapool.utils import find_executable

has_matlab = find_executable("matlab") is not None


def _run_conversion(interpreter_name, script, data_path, config):
    folder = data_path("test_landing_zone/data/FloDar/FloDar_%s/" % interpreter_name)
    raw_data_path = os.path.join(folder, "raw_data", "data-001.raw")
    # section names are lower case:
    getattr(config, interpreter_name.lower()).executable = find_executable(interpreter_name)
    return ConversionRunner(config).run_conversion(script, raw_data_path)


def _run_matlab_conversion(script, data_path, config):
    return _run_conversion("matlab", script, data_path, config)


def _run_julia_conversion(script, data_path, config):
    return _run_conversion("julia", script, data_path, config)


def _run_python_conversion(script, data_path, config):
    return _run_conversion("python", script, data_path, config)


def _run_r_conversion(script, data_path, config):
    return _run_conversion("R", script, data_path, config)


def _dump_rows(rows, regtest_print):

    regtest_print("converted data file has {} rows".format(len(rows)))

    groups = defaultdict(list)
    for row in rows:
        groups[row["parameter"]].append(row)

    def p(row_dict):
        line = "{" + ", ".join("{}: {!r}".format(k, v) for (k, v) in sorted(row_dict.items())) + "}"
        regtest_print(line)

    for parameter in sorted(groups.keys()):
        rows = groups[parameter]
        for row in rows[:5]:
            p(row)
        regtest_print("...")
        for row in rows[-5:]:
            p(row)
        regtest_print()


@pytest.mark.skipif(not has_matlab, reason="no matlab interpreter found on your system")
def test_matlab_file_conversion(data_path, setup_logger, regtest_print, config):

    script = data_path("test_landing_zone/data/FloDar/FloDar_matlab/conversion.m")
    rows = _run_matlab_conversion(script, data_path, config)
    _dump_rows(rows, regtest_print)


@pytest.mark.skipif(not has_matlab, reason="no matlab interpreter found on your system")
def test_matlab_file_conversion_failing(data_path, config, regtest_logger):

    script = os.path.join(data_path("failing_scripts", "conversion.m"))

    with regtest_logger():
        with pytest.raises(InvalidOperationError):
            _run_matlab_conversion(script, data_path, config)


def test_julia_file_conversion(data_path, setup_logger, config, regtest_print):

    script = data_path("test_landing_zone/data/FloDar/FloDar_julia/conversion.jl")

    rows = _run_julia_conversion(script, data_path, config)
    _dump_rows(rows, regtest_print)


def test_julia_file_conversion_failing(data_path, config, regtest_logger, regtest_print):

    script = data_path("failing_scripts", "conversion_exceeds_dimensions.jl")

    with regtest_logger():
        with pytest.raises(InvalidOperationError) as e:
            _run_julia_conversion(script, data_path, config)
        regtest_print(e.value)


def test_julia_file_wrong_function_name(data_path, config, regtest_logger, regtest_print):

    script = data_path("failing_scripts", "wrong_function_name.jl")

    with regtest_logger():
        with pytest.raises(InvalidOperationError) as e:
            _run_julia_conversion(script, data_path, config)
        regtest_print(e.value)


def test_julia_file_wrong_module_name(data_path, config, regtest_logger, regtest_print):

    script = data_path("failing_scripts", "wrong_module_name.jl")
    with regtest_logger():
        with pytest.raises(InvalidOperationError) as e:
            _run_julia_conversion(script, data_path, config)
        regtest_print(e.value)


def test_julia_file_non_ascii_output(data_path, config, regtest_logger, regtest_print):

    script = data_path("failing_scripts", "non_ascii_output.jl")

    config.julia.executable = find_executable("julia")

    with regtest_logger():
        with pytest.raises(FormatError) as e:
            _run_julia_conversion(script, data_path, config)
        regtest_print(e.value)


def test_python_file_conversion(data_path, setup_logger, config, regtest_print):

    script = data_path("test_landing_zone/data/FloDar/FloDar_python/conversion.py")

    rows = _run_python_conversion(script, data_path, config)
    _dump_rows(rows, regtest_print)


def test_r_file_conversion(data_path, setup_logger, config, regtest_print):

    script = data_path("test_landing_zone/data/FloDar/FloDar_R/conversion.r")

    rows = _run_r_conversion(script, data_path, config)
    _dump_rows(rows, regtest_print)
