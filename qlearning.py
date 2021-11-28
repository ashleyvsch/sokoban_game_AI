import sokoban_structures
from global_constants import *
import helper
import printing
from type_hepler import SokobanGame
from random import randint

def _exploit_action(gamestate: SokobanGame) -> '???':
    pass

def _explore_action(gamestate: SokobanGame) -> '??':
    action = _get_random_action()
    if _is_valid_action(action, gamestate):
        return action
    else: 
        return STAY

def _is_valid_action(action: np.array, gamestate: SokobanGame) -> bool:
    '''
    determines valid actions for a particular state, if an action to move is
    not valid, then the action is STAY
    '''
    current_state = gamestate.agent
    state_given_action = current_state  + action
    if (helper.board_index(gamestate, state_given_action) == OPEN
        or helper.board_index(gamestate, state_given_action) == GOAL):
        return True
    else: 
        return False

def _get_random_action() -> 'action':
    value = randint(1, 4)
    if value == 1:
        return UP
    if value == 2:
        return DOWN
    if value == 3:
        return LEFT 
    if value == 4:
        return RIGHT

def building() -> None:
    file = 'data/simplegame.txt'
    s = sokoban_structures.Sokoban(file)    
    _explore_action(s)

if __name__ == '__main__':
    building()