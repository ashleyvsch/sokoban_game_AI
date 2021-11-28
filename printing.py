import sokoban_structures
from global_constants import *
from type_hepler import *

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

def print_q_table(gamestate: SokobanGame):
    '''
    Print out qtable in visual format (np arrays only allow
    elements to be single value floats or ints)
    '''
    cols = 5 # num actions + 1
    valid_states = gamestate._valid_states
    rows = len(valid_states)
    q_table = gamestate.q_table
    table_for_printing = q_table.tolist()
    for i in range(1, rows + 1):
        table_for_printing[i][0] = valid_states[i]
    for j in range(1, 4 + 1):
        if j == 1:
            table_for_printing[0][j] = 'UP'
        if j == 2:
            table_for_printing[0][j] = 'DOWN'
        if j == 3:
            table_for_printing[0][j] = 'LEFT'
        if j == 4:
            table_for_printing[0][j] = 'RIGHT'      
    for i in range(rows):
        for j in range(cols):
            if i == 0 and j == 0:
                print('      ', end = '\t')
            elif type(table_for_printing[i][j]) == str:
                print(table_for_printing[i][j], end = '\t')
            elif j == 0:
                print(table_for_printing[i][j], end = '\t')
            else:
                print(round(table_for_printing[i][j],2), end = '\t')
        print()

def print_frequency_table(gamestate: SokobanGame):
    '''
    Print out frequency in visual format (np arrays only allow
    elements to be single value floats or ints)
    '''
    cols = 5 # num actions + 1
    valid_states = gamestate._valid_states
    rows = len(valid_states)
    frequency_table = gamestate.frequency_table
    table_for_printing = frequency_table.tolist()
    for i in range(1, rows + 1):
        table_for_printing[i][0] = valid_states[i]
    for j in range(1, 4 + 1):
        if j == 1:
            table_for_printing[0][j] = 'UP'
        if j == 2:
            table_for_printing[0][j] = 'DOWN'
        if j == 3:
            table_for_printing[0][j] = 'LEFT'
        if j == 4:
            table_for_printing[0][j] = 'RIGHT'      
    for i in range(rows):
        for j in range(cols):
            if i == 0 and j == 0:
                print('      ', end = '\t')
            elif type(table_for_printing[i][j]) == str:
                print(table_for_printing[i][j], end = '\t')
            else:
                print(round(int(table_for_printing[i][j]),2), end = '\t')
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