# encoding: utf-8
from __future__ import print_function, division, absolute_import

import os
import tempfile

from .errors import InvalidOperationError, InvalidConfiguration, DataPoolIOError, FormatError
from .julia_runner import JuliaRunner
from .matlab_runner import MatlabRunner
from .python_runner import PythonRunner
from .r_runner import RRunner
from .uniform_file_format import read_from_file, read_from_string, check_rows
from .utils import iter_to_list

RUNNERS = {
    '.m': (MatlabRunner, 'matlab'),
    '.jl': (JuliaRunner, 'julia'),
    '.py': (PythonRunner, 'python'),
    '.r': (RRunner, 'r'),
}

SUPPORTED_EXTENSIONS = RUNNERS.keys()


class ScriptRunnerFactory:
    def __init__(self, config):
        self.cached_runners = {}
        self.config = config

    def get_runner(self, path_to_script):
        __, ext = os.path.splitext(path_to_script)
        if ext in self.cached_runners:
            return self.cached_runners[ext]

        if ext not in RUNNERS.keys():
            raise InvalidOperationError("do not know how to run script {}.".format(path_to_script))

        runner_class, config_section = RUNNERS[ext]
        try:
            section = getattr(self.config, config_section)
        except KeyError:
            msg = "configuration {} has no section {}".format(self.config.__file__, config_section)
            raise InvalidConfiguration(msg)

        try:
            exe = section.executable
        except KeyError:
            msg = ("configuration {} has no field 'executable' in "
                   "section {}").format(self.config.__file__, config_section)
            raise InvalidConfiguration(msg)

        if exe.strip() == "":
            raise InvalidConfiguration("executable in section {} is not configured"
                                       .format(config_section))

        r = runner_class(exe)
        r.start_interpreter()
        self.cached_runners[ext] = r
        return self.cached_runners[ext]


class ConversionRunner:
    def __init__(self, config):
        self.script_runner_factory = ScriptRunnerFactory(config)
        self.config = config

    def _run_conversion(self, path_to_script, raw_data_path, verbose=False):

        try:
            raw_data_file_content = open(raw_data_path, "rb").read()
        except IOError as e:
            raise DataPoolIOError("could not read raw data: {}".format(e))

        runner = self.script_runner_factory.get_runner(path_to_script)

        # we create a tempfolder which encodes the path to the conversion script:
        tmpfldr = os.path.join(tempfile.tempdir,
                               path_to_script.replace("/", "__").replace(".", "_"))
        os.makedirs(tmpfldr, exist_ok=True)

        in_file = os.path.join(tmpfldr, "raw_data.txt")
        out_file = os.path.join(tmpfldr, "out_data.txt")

        # write raw data to temp file:
        try:
            with open(in_file, "wb") as fh:
                fh.write(raw_data_file_content)
        except IOError as e:
            raise DataPoolIOError("could not write raw data to {}. reason: {}"
                                  .format(in_file, e)) from None

        # run conversion script
        try:
            exit_code = runner.run_script(path_to_script, in_file, out_file, verbose=verbose)
        except NameError:
            raise
        except Exception as e:
            raise InvalidOperationError("running script failed. reason: {}".format(e)) from None

        if exit_code != 0:
            raise InvalidOperationError("running script failed. exit_code is {}.".format(
                exit_code)) from None

        # check if output file exists and can be opened for reading.
        try:
            with open(out_file, "r", encoding="ascii") as fh:
                content = fh.read()
        except IOError as e:
            raise DataPoolIOError("created output file {} is not readable. reason: {}"
                                  .format(out_file, e)) from None
        except UnicodeDecodeError as e:
            raise FormatError("created output file {} contains non-ascii chraracters: {}"
                              .format(out_file, e)) from None

        return content

    def run_conversion(self, script_path, raw_data_path, verbose=False):
        data = self._run_conversion(script_path, raw_data_path, verbose)
        try:
            rows = read_from_string(data)
        except ValueError as e:
            raise FormatError("reading result from {}: {}".format(script_path, e))
        msgs = check_rows(rows)
        if msgs:
            raise FormatError("{} errors in result from {}. first is: {}"
                              .format(len(msgs), script_path, msgs[0]))

        return rows

    @iter_to_list
    def check_conversion(self, script_path, raw_data_path, verbose):
        output_file = None
        try:
            data = self._run_conversion(script_path, raw_data_path, verbose)
        except Exception as e:
            yield Exception("could not run script: {}".format(e))
            return

        output_file = os.path.join(tempfile.mkdtemp(), "output.csv")
        with open(output_file, "w") as fh:
            fh.write(data)
        try:
            rows = read_from_file(output_file)
        except Exception as e:
            yield Exception("reading output failed: {}".format(e))
            return

        msgs = check_rows(rows)
        for i, msg in enumerate(msgs):
            if i >= 10:
                yield Exception("... skip remaining {} / {} msgs".format(len(msgs) - i, len(msgs)))
                return
            yield Exception("invalid output file {}: {}".format(output_file, msg))
            return

        yield output_file, rows
