'''
Here, we control the board,the agent, the actions! The object of the class can be updated
using public methods. Some things aren't meant to change (walls, goal locations) 
and some things definitely are (agent location, box locations)
'''

import numpy as np
from global_constants import *
from custom_errors import *
from pathlib import Path
import sys
import box_checking
import dead_locks

class Sokoban:
    '''
    A class that defines the Sokoban game we wish to play. Key elements are
    the board, the number of rows and columns, and lists of the attributes. 
    Key attributes are boxes (list of tuples), goals (list of tuples), and 
    the agent (a tuple)
    To initialize the object -- give a file path (str) that defines the game. 
    '''

    '''
    IMPORTANT: After reading everything in from the file (which has indices start
               from 1), EVERYTHING starts from 0)
    '''

    def __init__(self, path: str):
        '''
        requires initial game file that has been parsed and read and is 
        only a list of lines at the point of entry
        '''
    # -------------------------------------------------------- #
    # -------------- This is setup of the board! ------------- #
    # -------------------------------------------------------- #
        self._initial_gamestate = self._get_game_from_file(path)
        # initial_gamestate is a list where each element is a line from the file
        # in sting format
        game_size = map(int,self._initial_gamestate[0].split())
        self.num_rows, self.num_cols = game_size
        self.board = np.zeros(shape=(self.num_rows,self.num_cols), dtype=int) 

        self.agent = np.array([0,0])

        self.initialize_gamestate()

        self.num_goals = int(self._initial_gamestate[2].split()[0])
        self.num_boxes_on_goals = 0

    # -------------------------------------------------------- #
    # -------------------------------------------------------- #

    # -------------------------------------------------------- #
    # ----------- These are methods for updates! ------------- #
    # ---------- (public functions for the class) ------------ #
    # -------------------------------------------------------- #

    def is_terminal(self) -> bool:
        ''' 
        Terminal if there is a deadlock or you the 
        board has been solved
        '''
        if self.is_terminal_because_deadlock() or self.is_terminal_because_goalstate():
            return True
        else:
            return False

    def is_terminal_because_goalstate(self) -> bool:
        '''
        If all the boxes are on the goals, the agent 
        has solved the board
        '''
        if box_checking.is_all_boxes_on_goals(self.board, self.num_goals):
            return True
        else:
            return False

    def is_terminal_because_deadlock(self) -> bool:
        '''
        Deadlock occurs when a box is pushed somewhere that 
        makes the board unsolvable no matter what the agent
        does
        '''
        if dead_locks.dead_lock(self.board):
            return True
        else:
            return False
    
    def update_num_boxes_on_goals(self) -> int:
        self.num_boxes_on_goals = box_checking.check_box_on_goals(self.board)
        
    def move_agent(self, move: np.array):
        '''
        Move agent using an action. The input is a direction based on matrix
        notation of the board (up is -1, down is 1, right is 1, left is -1). The
        agent itself is updated but not the board!! This is meant to be used 
        when the action is decided and the move is *valid*!

        To avoid complexity of an agent walking over a goal, we don't update the 
        board with the agents location, we strictly change the agent's coordinates
        '''
        self.agent = self.agent + move
        return self.agent
    
    def board_with_agent(self):
        agent_location = self.agent
        board_with_agent = np.copy(self.board)
        board_with_agent[agent_location[0]][agent_location[1]] = AGENT
        return board_with_agent
    
    def take_action(self, action) -> int:
        '''
        Change the game board based on an action and return the result
        of the action
        - If the agent moves to a box, we move that box. It is already checked
          previously that the mox movement is allowed
        - This returns an integer relating to the agents move:
            OPEN:           moved to open space (not so good..)
            BOX:            moved a box to an open space (good!)
            BOX_ON_GOAL:    moved a box onto a goal (really good!)
            GOAL:           moved a box off a goal, so not it is in a goal space (bad!) 
        '''
        new_agent_state = self.move_agent(action)
        
        # if the agent is moving a box, we have to determine
        # if the box is on a goal or not
        if self.board[new_agent_state[0]][new_agent_state[1]] == BOX:
            self.board[new_agent_state[0]][new_agent_state[1]] = OPEN
            new_box_location = new_agent_state + action
            if self.board[new_box_location[0]][new_box_location[1]] == GOAL:
                self.board[new_box_location[0]][new_box_location[1]] = BOX_ON_GOAL
                if box_checking.is_all_boxes_on_goals(self.board, self.num_goals):
                    # agent has moved a box to solve the board
                    result = ALL_BOXES_ON_GOAL
                else:
                    if dead_locks.dead_lock(self.board):
                        # agent has pushed a box to a deadlock
                        result = DEADLOCK
                    else:
                        # agent has put a box on a goal
                        result = BOX_ON_GOAL
            elif self.board[new_box_location[0]][new_box_location[1]] == OPEN:
                self.board[new_box_location[0]][new_box_location[1]] = BOX
                if dead_locks.dead_lock(self.board):
                    # agent has pushed a box to a deadlock
                    result = DEADLOCK
                else:
                    # agent has successfully moved a box
                    result = BOX
            elif self.board[new_box_location[0]][new_box_location[1]] == WALL:
                raise BoxMoveError
        elif self.board[new_agent_state[0]][new_agent_state[1]] == BOX_ON_GOAL:
            # tha agent is moving a box off the goal 
            self.board[new_agent_state[0]][new_agent_state[1]] = GOAL
            new_box_location = new_agent_state + action
            if self.board[new_box_location[0]][new_box_location[1]] == GOAL:
                self.board[new_box_location[0]][new_box_location[1]] = BOX_ON_GOAL
                # the case when an agent is moving a box from one goal
                # to another
                result = BOX_ON_GOAL
            else:
                # the agent is moving a box off a goal
                self.board[new_box_location[0]][new_box_location[1]] = BOX
                result = GOAL
        else:
            # just a normal move
            result = OPEN

        self.valid_actions = self._get_valid_actions()

        return result
        
    def is_valid_action(self, action: np.array) -> bool:
        '''
        determines valid actions for a particular state
        '''
        current_agent_location = self.agent
        state_given_action = current_agent_location + action
        state_given_action_board_value = self.board[state_given_action[0],state_given_action[1]]
        if state_given_action_board_value == WALL:
            return False
        elif state_given_action_board_value == OPEN:
            return True
        elif state_given_action_board_value == BOX:
            resulting_box_location = current_agent_location + 2*action
            box_state_given_action_board_value = self.board[resulting_box_location[0],resulting_box_location[1]]
            if box_state_given_action_board_value == OPEN or box_state_given_action_board_value == GOAL:
                return True
            else: return False
    
    def _get_valid_actions(self) -> dict:
        '''
        Get the valid actions for an agent from a particular board location
        and return a dictionary of the valid actions
        '''

        current_agent_location = np.copy(self.agent)
        valid_action = {}

        possible_actions = [UP, DOWN, RIGHT, LEFT, BOX_UP, BOX_DOWN, BOX_RIGHT, BOX_LEFT]

        for i in range(1,5):
            action = possible_actions[i-1]
            possible_location_index = current_agent_location + action
            possible_location = self.board[possible_location_index[0], possible_location_index[1]]
            if possible_location != WALL:
                box_resulting_location_index = current_agent_location + 2*action
                possible_box_location = self.board[box_resulting_location_index[0], box_resulting_location_index[1]]
                if possible_location == OPEN or possible_location == GOAL:
                    valid_action[i] = action
                elif ((possible_location == BOX and possible_box_location == OPEN) 
                        or (possible_location == BOX and possible_box_location == GOAL)
                        or (possible_location == BOX_ON_GOAL and possible_box_location == GOAL)):
                    valid_action[i+4] = action

        return valid_action

    def initialize_gamestate(self):
        '''
        This function is used to initialize the game state board, as well as reset the
        board to its original state.
        '''
        # this is the board - it is a numpy 2d array initialized to all zeros and 
        # will be filled in accordingly...
        self.board = np.zeros(shape=(self.num_rows,self.num_cols), dtype=int)
        # second element of gamestate should be a list of coordinates
        # of wall squares where the first element is the number of wall 
        # squares
        self._setup_wall_squares(self._initial_gamestate[1])
        # third element of gamestate should be a the number of boxes followed
        # by their coordinates
        self._setup_boxes(self._initial_gamestate[2])
        # fourth element of gamestate should be the number of storage locations
        # followed by their coordinates
        self._setup_goal(self._initial_gamestate[3])
        # fifth element is the agents location
        self._setup_agent(self._initial_gamestate[4])
        self.valid_actions = self._get_valid_actions()

    # -------------------------------------------------------- #
    # -------------------------------------------------------- #

    # -------------------------------------------------------- #
    # ------ These are methods for initialization! ----------- #
    # -------- (private functions for the class) ------------- #
    # -------------------------------------------------------- #

    def _get_game_from_file(self, file_path: str) -> list:
        '''
        Gets the initial game setup from a file path and returns a list 
        that can be printed to view the game
        '''
        game_setup_file = None
        try:
            file_path = Path(file_path)
            if not file_path.is_file():
                raise FileNotFoundError
            game_setup_file = file_path.open( 'r')
            file_contents = []
            for line in game_setup_file:
                if line != '':
                    if line.endswith('\n'):
                        line = line[:-1]
                        file_contents.append(line)
                    else:
                        file_contents.append(line)
            if len(file_contents) != 5:
                raise InvalidFileError
        except InvalidFileError:
            print('\nERROR!')
            print('The file you gave:', file_path, 'is not in the correct')
            print('format. We expect the format to be exactly 5 lines.\n')
            sys.exit()
        except FileNotFoundError:
            print('\nERROR!')
            print('Tried to find the file', file_path, 'and failed...')
            print('Are you sure this file exists?\n')
            sys.exit()
        finally:
            if game_setup_file != None:
                game_setup_file.close()
        return file_contents

    def _setup_wall_squares(self, wall_info: str):
        '''
        Use the information in wall_info to initialize the wall squares into
        the board
        '''
        wall_squares = wall_info.split()
        num_wall_squares = int(wall_squares.pop(0))
        for i in range(0, 2*num_wall_squares, 2):
            x = int(wall_squares[i]) 
            y = int(wall_squares[i+1]) 
            self.board[x-1][y-1] = WALL 

    def _setup_boxes(self, box_info: str):
        '''
        Use the information in box_info to initialize the boxes into
        the board
        '''
        box_squares = box_info.split()
        num_box_squares = int(box_squares.pop(0))
        for i in range(0, 2*num_box_squares, 2):
            x = int(box_squares[i]) 
            y = int(box_squares[i+1]) 
            self.board[x-1][y-1] = BOX

    def _setup_goal(self, goal_info: str):
        '''
        Use the information in goal_info to initialize the goals into
        the board
        '''       
        goal_squares = goal_info.split()
        num_goal_squares = int(goal_squares.pop(0))        
        for i in range(0, 2*num_goal_squares, 2):
            x = int(goal_squares[i])
            y = int(goal_squares[i+1])
            self.board[x-1][y-1] = GOAL
    
    def _setup_agent(self, agent_info: str):
        '''
        Use the information in agent_info to initialize the agent into
        the board
        '''        
        agent_square = agent_info.split()
        agent_square = map(int,agent_square)
        x, y = agent_square
        self.agent = np.array([x-1, y-1])
    # -------------------------------------------------------- #
    # -------------------------------------------------------- #


