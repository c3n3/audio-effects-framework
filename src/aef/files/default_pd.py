from aef.constants import Constants
name = "{}default.pd".format(Constants.DEFAULT_PD_DIR)
file = """
#N canvas 72 96 1848 984 12;
#X obj 209 25 *~ 1.0001;
#X obj 208 267 *~ 1.0002;
#X obj 392 70 route volume;
#X floatatom 377 144 5 0 0 0 - - -;
#X connect 0 0 1 0;
#X connect 2 0 3 0;
#X connect 3 0 1 1;
"""