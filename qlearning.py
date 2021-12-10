'''
The Q-Learning algorithm that uses the data types
q learner and sokoban
'''

from custom_errors import NotOptimalAction, ValuesTooBigError
from qlearner import QLearner
import printing
from custom_errors import *
import numpy as np
from global_constants import *

def q_learning(q_learner: QLearner, num_trials: int, max_steps: int) -> list or None:
    best_actions = None
    best_num_steps = max_steps
    solution = False
    for episode in range(num_trials):
        q_learner.initialize_gamestate()
        step = 0
        actions = []
        while not q_learner.is_terminal() and step < max_steps:

            current_state = q_learner.agent
            action = q_learner.epsilon_greedy()
            reward, new_state = q_learner.observe_action(action)
            q_learner.update_q_value(current_state, new_state, action, reward)
            actions.append(action)
            step += 1

        if ((step < best_num_steps) and 
                not q_learner.is_terminal_because_deadlock()):
            if solution == False:
                solution = True
                episode_number = episode
                number_of_steps_first = len(actions)
            best_num_steps = step
            best_actions = actions

            # if you want to end trial when a solution 
            # is found uncomment break
            # break

        # I like to print these things usually
        # ------------------
        # ------------------
        # print('Episode:', episode+1, 
        #     '\tNumber of Steps:', step, 
        #     '\tSolution:', q_learner.is_terminal_because_goalstate())
        # printing.print_game(q_learner)

    # if solution == True:
    #     print('A solution was first found on episode', episode_number, 
    #             'in', number_of_steps_first, 'steps')

    return best_actions