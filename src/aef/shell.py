from aef.log import _report
import subprocess as sp
import inspect
import os

def run(command, expectFail=False, shell=False, background=False, debug=False):
    if not background:
        result = sp.run(command, stdout=sp.PIPE, stderr=sp.PIPE, shell=shell)
        # Custom log to report caller of this function up stack 3 funcs
        if debug:
            _report("Debug", 2, result.stdout)
        if not expectFail and result.returncode != 0:
            _report("Error", 2,
                f"""
    Command '{' '.join(command)}' failed:
    --------------------------------------
    stdout:
    {result.stdout.decode('UTF-8')}
    stderr:
    {result.stderr.decode('UTF-8')}
    --------------------------------------""")
        return result
    else:
        return sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, shell=shell)
