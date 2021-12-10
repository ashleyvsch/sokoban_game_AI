'''
Global constants defining board possibilities and actions
'''

import numpy as np

# Feel free to modify these constants to test the algorithm
# --------------------------------------------------------

GAMMA = 0.99
ALPHA = 0.01
EPSILON = 0.1

MOVE_PENALTY = -0.1
MOVE_BOX_REWARD = -0.1
BOX_ON_GOAL_REWARD = 1
SOLVE_GAME_REWARD = 2 
DEADLOCK_PENALTY = -0.5

'''
Note on gamma:
If we set gamma to zero, the agent completely ignores the future rewards. 
Such agents only consider current rewards. On the other hand, if we set 
gamma to 1, the algorithm would look for high rewards in the long term.
'''
'''
Note on alpha:
If we set alpha to zero, the agent learns nothing from new actions. 
Conversely, if we set alpha to 1, the agent completely ignores prior 
knowledge and only values the most recent information. Higher alpha 
values make Q-values change faster.
'''
'''
Note on epsilon:
If epsilon is set to 0, we never explore but always exploit the knowledge 
we already have. On the contrary, having the epsilon set to 1 force the 
algorithm to always take random actions and never use past knowledge. Usually, 
epsilon is selected as a small number close to 0.
'''

# DON'T CHANGE ANYTHING BELOW THIS LINE
# -------------------------------------

INVALID = 6
OPEN = 0
WALL = 1
BOX = 2
GOAL = 3
AGENT = 4
BOX_ON_GOAL = 5
ALL_BOXES_ON_GOAL = 6
DEADLOCK = 7
NO_MOVE = -1

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
RIGHT = np.array([0, 1])
LEFT = np.array([0, -1])
BOX_UP = np.array([-1, 0])
BOX_DOWN = np.array([1, 0])
BOX_RIGHT = np.array([0, 1])
BOX_LEFT = np.array([0, -1])
STAY = np.array([0, 0])