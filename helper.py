import sokoban_structures
from global_constants import *
from type_hepler import *

# i need to create a function to write to file

def print_game(gamestate: SokobanGame):
    '''
    Print out current game state in a visual formal
    '''
    # will eventually probs convert this to write file since thats what we need
    cols = gamestate.num_cols
    rows = gamestate.num_rows
    for i in range(cols):
        for j in range(rows):
            square = gamestate.board[i,j]
            if square == OPEN:
                print(' ', end='')
            elif square == WALL:
                print('#', end='')
            elif square == BOX:
                print('$', end='')
            elif square == GOAL:
                print('.', end='')
            elif square == AGENT:
                print('@', end='')
        print()

def print_choices(choices: list[MoveArray]):
    '''
    Print a sting containg firsly the number of total moves then a sequence
    of moves where up: 'U', down: 'D', right: 'R', left: 'L'.
    '''
    num_moves = len(choices)
    final_string = str(num_moves)
    for move in choices:
        if np.array_equal(move, UP):
            final_string += ' U'
        elif np.array_equal(move, DOWN):
            final_string += ' D'
        elif np.array_equal(move, RIGHT):
            final_string += ' R'
        elif np.array_equal(move, LEFT):
            final_string += ' L'
        else:
            raise ValueError('Invalid Move?? Something is very wrong')
    print(final_string)

def move_choice(s: SokobanGame) -> list[MoveArray]:
    '''
    Determines the optimal policy based off the utilities of a current game
    state. Should be ran after the utilities have been determined by some
    algorithm (such as value iteration, for example)
    '''
    choices = []
    while not s.agent_in_goal():
        agent_location = s.agent
        possible_choices = [UP,  DOWN, RIGHT, LEFT]
        utility_with_choice = dict()
        for choice in possible_choices:
            resulting_state = agent_location + choice
            utility_of_choice = utility_value(s, resulting_state)
            if not np.isnan(utility_of_choice):
                utility_with_choice[utility_of_choice] = choice
        decision = max(utility_with_choice)
        s.update_agent(utility_with_choice[decision])
        choices.append(utility_with_choice[decision])
        print_game(s)
    return choices

def board_index(s: SokobanGame, location: StateArray):
    '''
    Returns the true board index given a sokoban state and some location. 
    Minimizes the effort to keep track of array index vs visual board index.
    '''
    return s.board[location[0] - 1][location[1] - 1]

def reward_value(s: SokobanGame, location: StateArray):
    '''
    Returns the true reward index given a sokoban state and some location. 
    Minimizes the effort to keep track of array index vs visual reward index.
    '''
    return s.rewards[location[0] - 1][location[1] - 1]

def utility_value(s: SokobanGame, location: StateArray):
    '''
    Returns the true utility index given a sokoban state and some location. 
    Minimizes the effort to keep track of array index vs visual utility index.
    '''
    return s.utilities[location[0] - 1][location[1] - 1]