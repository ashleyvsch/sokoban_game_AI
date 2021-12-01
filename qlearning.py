from custom_errors import NotOptimalAction, ValuesTooBigError
from qlearner import QLearner
import printing
from custom_errors import *

def main() -> None:
    '''
    executable function to execute q learning
    '''

    file = 'data/simplegame2.txt'
    
    q = QLearner(file)

    num_trials = 200
    max_steps = 100

    q_learning(q, num_trials, max_steps)

    try:
        actions = q.get_optimal_policy()
        printing.print_choices(actions)
    except NotOptimalAction:
        pass

    '''
    print(q.board_with_agent())
    printing.print_game(q)
    printing.print_q_table(q)
    '''

def q_learning(q_learner: QLearner, num_trials: int, max_steps: int):
    for episode in range(num_trials):
        initial_game = q_learner.initialize_gamestate()
        step = 0
        while not q_learner.is_terminal() and step < max_steps:
            current_state = q_learner.agent
            action = q_learner.epsilon_greedy()
            reward, new_state = q_learner.observe_action(action)
            q_learner.update_q_value(current_state, new_state, action, reward)
            step += 1
        print('Number of Steps Used:', step)

if __name__ == '__main__':
    main()