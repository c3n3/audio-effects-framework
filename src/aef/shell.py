# Audio Effects Framework - A python library to setup Puredata effects
# Copyright (C) 2022  Caden Churchman
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
            _report(
                "Error",
                2,
                f"""
    Command '{' '.join(command)}' failed:
    --------------------------------------
    stdout:
    {result.stdout.decode('UTF-8')}
    stderr:
    {result.stderr.decode('UTF-8')}
    --------------------------------------""",
            )
        return result
    else:
        return sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, shell=shell)
