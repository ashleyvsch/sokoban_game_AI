# some modules from the python library
import numpy as np
# modules that should be in this directory follow
# this line
import sokoban_structures
import helper
import printing
from global_constants import *
from custom_errors import *
from type_hepler import *


np.set_printoptions(precision=4, suppress=True)

def main():

    file = 'data/simplegame.txt'
    s = sokoban_structures.Sokoban(file)
    printing.print_game(s)

    ### all this does is get the utilities -- no attribute of the
    ### game is changed besides s.utilities (the np.ndarray that has the
    ### utilities)
    value_iteration(s, 1E-4)

    # get the moves based off the utilities
    moves = helper.move_choice(s)
    # print(moves)
    printing.print_choices(moves)
    print(s.utilities)


def value_iteration(s: SokobanGame, epsilon: float) -> SokobanUtilities:
    '''
    Value iteration program (Figure 17.6 in the text)
    '''
    delta = 0
    count = 0
    while delta <= epsilon*(1-GAMMA)/GAMMA:
        # loop through all possible states
        for m in range(s.num_rows):
            for n in range(s.num_cols):
                current_state = np.array([m,n])
                old_utility = s.utilities[m][n]
                if (helper.board_index(s, current_state) == OPEN 
                    or helper.board_index(s, current_state) == AGENT):
                    actions = valid_actions(current_state, s)
                    qs = []
                    for intended_action in actions:
                        qs.append(q_value(s, current_state, actions, intended_action))
                    new_utility = max(qs)
                    s.update_utility(current_state, new_utility)
                    if new_utility-old_utility > delta:
                        delta = new_utility - old_utility
        count += 1
    # print('Number of iterations is:', count)
    return s.utilities


def q_value(s: SokobanGame, state: StateArray, 
                    actions: list[MoveArray], intended_action: MoveArray) -> float:
    '''
    Determines the q-value given a sokoban type, a state, and valid actions
    for that state.
    '''
    if len(actions) != 4:
        raise ValueError('There should be four possible actions exactly')
    sum = 0
    p = probability(actions, intended_action)
    for i in range(len(actions)):
        state_given_action = state + actions[i]
        sum += p[i] * (helper.reward_value(s,state_given_action) + GAMMA * 
            helper.utility_value(s,state_given_action))
    return sum
        

def probability(valid_actions: list, intended_action: MoveArray) -> list[float]:
    '''
    Determines the probability of each action. 
    '''
    if len(valid_actions) != 4:
        raise ValueError('There should be four possible actions exactly')
    probabilities = []
    for a in valid_actions:
        if np.array_equal(a, intended_action):
            probabilities.append(0.7)
        else:
            probabilities.append(0.1)
    return probabilities


def valid_actions(state: StateArray, s: SokobanGame) -> list:
    '''
    determines valid actions for a particular state, if an action to move is
    not valid, then the action is STAY
    '''
    all_actions = [UP, DOWN, RIGHT, LEFT]
    valid_actions = []
    for a in all_actions:
        state_given_action = state + a
        if (helper.board_index(s, state_given_action) == OPEN
            or helper.board_index(s, state_given_action) == GOAL):
            valid_actions.append(a)
        else: 
            # if the action isn't allowed, you end up 
            # right where you were
            valid_actions.append(STAY)
    return valid_actions


if __name__ == '__main__':
    main()