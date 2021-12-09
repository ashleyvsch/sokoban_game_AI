from custom_errors import NotOptimalAction, ValuesTooBigError
from qlearner import QLearner
import printing
from custom_errors import *
import dead_locks
import numpy as np
import box_checking
from global_constants import *

def main() -> None:
    '''
    executable function to execute q learning
    '''

    # file = 'data/simplegame3.txt'
    # file = 'data/trial2.txt'
    # file = 'data/sokoban01.txt'
    # file = 'data/sokoban-04.txt'
    file = 'data/sokoban-04.txt'
    # file = 'data/my_trials_01.txt'
    # file = 'data/my_trials_02.txt'
    # file = 'data/sokoban-02.txt'
    # file = 'data/sokoban-03.txt'
    # file = 'data/sokoban-04c.txt'
    file = 'data/sokoban03.txt'
    
    q = QLearner(file)

    printing.print_game(q)

    num_trials = 1000
    max_steps = 1000

    actions = q_learning(q, num_trials, max_steps)
    if actions == None:
        print('No solution was found')
    else:
        printing.print_choices(actions)

    '''
    up = 1, 5
    down = 2, 6
    right = 3, 7
    left = 4, 8
    '''
    # actions = [DOWN, DOWN, LEFT, LEFT, LEFT, LEFT, LEFT, UP, UP, RIGHT, RIGHT, RIGHT, RIGHT]
    # actions = [DOWN, DOWN, LEFT, LEFT, LEFT, UP, UP, DOWN, DOWN, LEFT, LEFT, UP, RIGHT, DOWN, RIGHT, UP, LEFT, LEFT, UP, UP, RIGHT, DOWN, RIGHT, RIGHT, RIGHT, LEFT, LEFT, DOWN, DOWN, RIGHT, RIGHT, RIGHT, UP, UP, LEFT, LEFT, LEFT, LEFT, DOWN, LEFT, DOWN, ]
    # actions = [DOWN, DOWN, LEFT, LEFT, LEFT, UP, UP, DOWN, LEFT]
    # actions = [3, 3, 3, 1, 1, 1, 1, 4, 4, 4, 2, 7, 7, 7, 7, 7, 1, 3, 6, 6]
    # for action in actions:
    #     print('----')
    #     current_state = q.agent
    #     reward, new_state = q.observe_action(action)
    #     q.update_q_value(current_state, new_state, action, reward)
    #     print('reward', reward)
    #     printing.print_game(q)
        # print('vaild actions', q.valid_actions)
        # print('action taken', action)
        # printing.print_q_table(q)

    # valid_actions =  q.get_valid_actions()
    # print(valid_actions)    
    # print(q._get_random_action(valid_actions))
    # current_state_index = q._get_state_index(q.agent)
    # print(q._get_q_values(current_state_index, valid_actions))

    


def q_learning(q_learner: QLearner, num_trials: int, max_steps: int):
    best_actions = None
    best_num_steps = max_steps
    solution = False
    for episode in range(num_trials):
        q_learner.initialize_gamestate()
        step = 0
        actions = []
        while not q_learner.is_terminal():
            # print('entered')
            if step > max_steps:
                break
            current_state = q_learner.agent
            action = q_learner.epsilon_greedy()
            reward, new_state = q_learner.observe_action(action)
            q_learner.update_q_value(current_state, new_state, action, reward)
            actions.append(action)
            step += 1
            # print(q_learner.num_goals)
            # printing.print_game(q_learner)
        if ((step < best_num_steps) and 
                not q_learner.is_terminal_because_deadlock()):
            if solution == False:
                solution = True
                episode_number = episode
                number_of_steps_first = len(actions)
            best_num_steps = step
            best_actions = actions
            for repeat in range(20):
                q_learner.initialize_gamestate()
                for i in range(len(actions)):
                    current_state = q_learner.agent
                    do_action = actions[i]
                    reward, new_state = q_learner.observe_action(do_action)
                    q_learner.update_q_value(current_state, new_state, do_action, reward)
        # print(q_learner.is_terminal_because_deadlock())
        print('Episode:', episode+1, '\tNumber of Steps:', step, '\tSolution:', q_learner.is_terminal_because_goalstate())
        # print('last reward:', reward)
        printing.print_game(q_learner)

        # if step > max_steps:
        #     break
    printing.print_q_table(q_learner)
    if solution == True:
        print('A solution was first found on episode', episode_number, 'in', number_of_steps_first, 'steps')
    return best_actions

if __name__ == '__main__':
    main()