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

name = Constants.GLOBAL_PD
file = """
#N canvas -28 121 1124 625 12;
#X text 326 104 looper;
#X obj 461 186 readsf~;
#X obj 610 329 writesf~;
#X obj 554 190 bng 15 250 50 0 empty empty empty 17 7 0 10 -262144
-1 -1;
#X obj 571 16 netreceive 3000;
#X obj 628 253 adc~;
#X obj 499 486 dac~;
#X obj 512 421 *~ 1;
#X floatatom 761 314 5 0 0 0 - - -;
#X msg 97 240 \; pd dsp 1 \;;
#X obj 61 135 loadbang;
#X msg 593 189 open out.wav \, 1;
#X obj 568 49 route global_loop global_record global_volume global_playback
;
#X obj 552 234 readsf~;
#X obj 737 124 bng 15 250 50 0 empty empty empty 17 7 0 10 -262144
-1 -1;
#X msg 776 123 open playback.wav \, 1;
#X obj 536 281 *~ 0.85;
#X connect 1 0 16 0;
#X connect 1 1 3 0;
#X connect 3 0 11 0;
#X connect 4 0 12 0;
#X connect 5 0 2 0;
#X connect 5 1 2 0;
#X connect 7 0 6 0;
#X connect 7 0 6 1;
#X connect 8 0 7 1;
#X connect 10 0 9 0;
#X connect 11 0 1 0;
#X connect 12 0 1 0;
#X connect 12 1 2 0;
#X connect 12 2 8 0;
#X connect 12 3 13 0;
#X connect 13 0 16 0;
#X connect 13 1 14 0;
#X connect 14 0 15 0;
#X connect 15 0 13 0;
#X connect 16 0 2 0;
#X connect 16 0 7 0;
"""
