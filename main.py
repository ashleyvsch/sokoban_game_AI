'''
Reads command line argument and runs the trial
'''

from qlearner import QLearner
from qlearning import q_learning
import printing
import sys

def main() -> None:
    '''
    executable function to execute q learning
    - just choose a file, number of trials, and number of steps
    '''
    file = 'data/' + str(sys.argv[1])

    q = QLearner(file)

    # printing.print_game(q)

    num_trials = 1000
    max_steps = 200

    actions = q_learning(q, num_trials, max_steps)
    if actions == None:
        print('No solution was found')
    else:
        # print('The best solution found in the least number of steps is:')
        printing.print_choices(actions)   

if __name__ == '__main__':
    main() 