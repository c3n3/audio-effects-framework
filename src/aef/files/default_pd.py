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

from aef.constants import Constants
from aef.settings import GlobalSettings

name = "{}default.pd".format(Constants.DEFAULT_PD_DIR)
file = """
#N canvas 2320 186 1386 720 12;
#X obj 240 138 *~ 1.0001;
#X obj 233 289 *~ 1.0002;
#X obj 392 70 route __volume;
#X floatatom 377 144 5 0 0 0 - - - 0;
#X obj 260 237 *~ 5;
#X obj 391 32 inlet;
#X obj 138 41 inlet~;
#X obj 204 35 inlet~;
#X obj 215 392 outlet~;
#X obj 309 396 outlet~;
#X connect 0 0 4 0;
#X connect 1 0 8 0;
#X connect 1 0 9 0;
#X connect 2 0 3 0;
#X connect 3 0 1 1;
#X connect 4 0 1 0;
#X connect 5 0 2 0;
#X connect 6 0 0 0;
#X connect 7 0 0 0;

""".format(
    GlobalSettings.settings["scale_volume"]
)
