
## Create list of items considered objects

#X obj
#X floatatom
#N canvas

## Items that do not count:

#X restore


## Global variables that must be diluted

#X obj (r)
#X obj (s)
#X obj (table)
#X obj (array)
#X obj (delwrite)
#X obj (delread)

## Parse sliders to encoders

take name and range of sliders to give encoder input
- use special naming setup to do this


## Make patches subcanvases to be linked together