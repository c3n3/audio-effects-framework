from aef.constants import Constants
from aef.settings import GlobalSettings
name = Constants.TOP_PD
file = """
#N canvas 996 96 924 984 12;
#X obj 124 331 dac~;
#X obj 222 16 netreceive 2998;
#X obj 222 107 route on off;
#X msg 459 25 on;
#X msg 576 29 off;
#X msg 331 181 \; pd-master.pd menuclose;
#X msg 18 184 \; pd open master.pd {} 1;
#X connect 1 0 2 0;
#X connect 2 0 6 0;
#X connect 2 1 5 0;
#X connect 3 0 2 0;
#X connect 4 0 2 0;
#X connect 5 0 0 1;
#X connect 5 0 0 0;
""".format(GlobalSettings.settings['temp_dir'])
