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

NO_MOVE = -1

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
RIGHT = np.array([0, 1])
LEFT = np.array([0, -1])
STAY = np.array([0, 0])

GAMMA = 0.8
ALPHA = 0.1
EPSILON = 0.2


# was being used to check if q values blow up to stop them from 
# getting too large, but it isn't being used anywhere right now
PRECISION = 1E20

# just used to check for optimal policy... sometimes if the q table
# is messed and the actions aren't really optimal it will take lots
# of steps... just a safety measure
MAX_STEPS_ALLOWED_FOR_OPTIMAL = 30


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