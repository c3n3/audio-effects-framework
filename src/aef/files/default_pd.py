from aef.constants import Constants
from aef.settings import GlobalSettings
name = "{}default.pd".format(Constants.DEFAULT_PD_DIR)
file = """
#N canvas 2320 186 1386 720 12;
#X obj 240 138 *~ 1.0001;
#X obj 233 289 *~ 1.0002;
#X obj 392 70 route volume;
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

""".format(GlobalSettings.settings['scale_volume'])