from aef.constants import Constants
from aef.settings import GlobalSettings
name = Constants.TOP_PD
file = """
#N canvas 636 478 924 984 12;
#X obj 222 16 netreceive 2998;
#X obj 222 107 route on off;
#X msg 459 25 on;
#X msg 576 29 off;
#X msg 331 181 \; pd-master.pd menuclose;
#X msg 18 184 \; pd open master.pd {} 1;
#X obj 399 109 adc~;
#X obj 207 287 loadbang;
#X msg 209 366 \; pd dsp 1 \;;
#X connect 0 0 1 0;
#X connect 1 0 5 0;
#X connect 1 1 4 0;
#X connect 2 0 1 0;
#X connect 3 0 1 0;
#X connect 7 0 8 0;
""".format(GlobalSettings.settings['temp_dir'])
