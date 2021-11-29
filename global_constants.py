'''
Global constants defining board possibilities and actions
'''

import numpy as np

INVALID = 6
OPEN = 0
WALL = 1
BOX = 2
GOAL = 3
AGENT = 4
BOX_ON_GOAL = 5

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
RIGHT = np.array([0, 1])
LEFT = np.array([0, -1])
STAY = np.array([0, 0])

GAMMA = 1