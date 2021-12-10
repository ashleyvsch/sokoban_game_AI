## Reinforcement Learning for the Sokoban Game

This project has been developed in python 3.9.7 with 
the dependency numpy

To run the program, follow the following steps from the 
root directory on the command line:

First activate the virtual environment and install dependencies:
[on macOS use `python3` not `python`]

```
$ cd env/bin
$ source activate
$ cd ../..
$ python -m pip install --upgrade pip
$ pip install numpy
```

Next run the program by choosing from any board located in
the data folder [the test will run 1000 trials to find the 
best possible solution within that timeframe]:

`$ python main.py <board name>`

Example run:

```
$ python main.py my_trials_01.txt
13 R R U L R R R D L L U L D
```

Choices are:

`sokoban00.txt`
`sokoban01.txt`
`sokoban-02.txt`
`sokoban-03.txt`
`sokoban-04.txt`
`sokoban-05a.txt`
`sokoban-04c.txt`
`my_trials_01.txt`
`my_trials_02.txt`
`my_trials_03.txt`

Note:
Some boards do better with different parameters (discount
factor, learning rate, reward values). These can be modified
in the `global_constants.py` file.

```
sokoban00.txt:

###
#@#
#$#
#.#
###
```

```
sokoban01.txt:

########
#. #   #
#  $   #
#   # ##
## # $.#
#   $  #
#  .# @#
########
```

```
sokoban-02.txt:

########
#  .# .#
# $   @#
# $$## #
#     .#
########
```

```
sokoban-03.txt

########
# $.# .#
#     @#
# $$#$ #
#    ..#
########
```

```
sokoban-04.txt

###########
#         #
# $       #
###   #.  #
# $$  #.  #
#@   ##.  #
###########
```

```
sokoban-05a.txt

############
#   #      #
#   #$#    #
#          #
###    $   #
#     ######
#  @   ..###
############
```

```
sokoban-04c.txt

###########
#         #
# $       #
###   #   #
#  $  #.  #
#@   ##.  #
###########
```

```
my_trials_01.txt:

#######
## .###
#.$$  #
#@ $  #
##. ###
#######
```

```
my_trials_02.txt

########
#  . . #
#    # #
## # # #
##  $  #
##  $@ #
##     #
##     #
########
```

```
my_trials_03.txt

#########
#.. $ ..#
#.  $  .#
#  $ $  #
#$$ @ $$#
#  $ $  #
#.  $  .#
#.. $ ..#
#########
```