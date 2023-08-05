# encoding: utf-8
from __future__ import print_function, division, absolute_import

import os

from .interpreter_bridge import InterpreterBridge


class JuliaRunner(InterpreterBridge):

    NAME = "JULIA"
    EXTRA_ARGS = ["-i", "--startup-file=no"]

    MSG_MARKER = "!!!"

    TEMPLATE = """
    module _we_use_here_a_module_to_keep_the_workspace_clean
        exit_code__ = 0
        try
            {command}
        catch ex
            bt = catch_stacktrace()
            exit_code__ = 1
            println("{MSG_MARKER}ERROR:START")
            showerror(STDOUT, ex)
            println()
            for i = 1:length(bt)
                if contains(string(bt[i]), "in anonymous at")
                    break
                end
                println(bt[i])
            end
            println("{MSG_MARKER}ERROR:END")
        end
        println("{MSG_MARKER}EXITCODE:$(exit_code__)")
    end
    println("{MSG_MARKER}FINISHED")
    """

    def run_script(self, path_to_script, in_file_path, out_file_path, verbose=False):
        file_name = os.path.basename(path_to_script)

        script_folder = os.path.dirname(path_to_script)
        module_name, __ = os.path.splitext(file_name)

        code = """
        include("{path_to_script}")
        {module_name}.convert("{in_file_path}", "{out_file_path}")
        """.format(**locals())

        return self.run_command(code, verbose=verbose)

    def get_julia_version_string(self):
        self.p.stdin.write(b"VERSION\n")
        self.p.stdin.flush()
        result = self.p.stdout.readline().rstrip()
        assert result.startswith(b"v"), 'got %r, expected a string like v"0.5.0"' % result
        return str(result.lstrip(b"v").strip(b'"'), encoding="ascii")
