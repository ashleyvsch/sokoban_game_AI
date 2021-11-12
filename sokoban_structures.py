'''
The bulk of the project design is within the Sokoban class. Here, we control the board,
the agent, the utilities, rewards, and everything! The object of the class can be updated
using public methods. Some things aren't meant to change (walls, goal locations, rewards) 
and some things definitely are (agent location, utility values, box locations)
'''

import numpy as np
from global_constants import *
from custom_errors import *
from pathlib import Path
import sys

class Sokoban:
    '''
    A class that defines the Sokoban game we wish to play. Key elements are
    the board, the number of rows and columns, and lists of the attributes. 
    Key attributes are boxes (list of tuples), goals (list of tuples), and 
    the agent (a tuple)
    To initialize the object -- give a file path (str) that defines the game. 
    '''

    def __init__(self, path: str):
        '''
        requires initial game file that has been parsed and read and is 
        only a list of lines at the point of entry
        '''
    # -------------------------------------------------------- #
    # -------------- This is setup of the board! ------------- #
    # -------------------------------------------------------- #
        _initial_gamestate = self._get_game_from_file(path)
        # initial_gamestate is a list where each element is a line from the file
        # in sting format
        game_size = map(int,_initial_gamestate[0].split())
        self.num_rows, self.num_cols = game_size
        # this is the board - it is a numpy 2d array
        self.board = np.zeros(shape=(self.num_rows,self.num_cols), dtype=int) 
        # these will end up being lists of np arrays where the arrays are coordinates
        self.walls = []
        self.boxes = []
        self.goals = []
        # this is just a array of the agents current location
        self.agent = np.array([0,0])
        self.rewards  = np.zeros(shape=(self.num_rows,self.num_cols), dtype=float)
        self.utilities = np.zeros(shape=(self.num_rows,self.num_cols), dtype=float)

        # first element of gamstate should be size of game
        self._setup_wall_squares(_initial_gamestate[1])
        # second element of gamestate should be a list of coordinates
        # of wall squares where the first element is the number of wall 
        # squares
        self._setup_boxes(_initial_gamestate[2])
        # third element of gamestate should be a the number of boxes followed
        # by their coordinates
        self._setup_goal(_initial_gamestate[3])
        # fourth element of gamestate should be the number of storage locations
        # followed by their coordinates
        self._setup_agent(_initial_gamestate[4])
        # reward are setup depending on the state of the board so it is 
        # initialized last
        self._setup_rewards()
        self._setup_utilities()
    # -------------------------------------------------------- #
    # -------------------------------------------------------- #

    # -------------------------------------------------------- #
    # ----------- These are methods for updates! ------------- #
    # ---------- (public functions for the class) ------------ #
    # -------------------------------------------------------- #
    def agent_in_goal(self) -> bool:
        for goal in self.goals:
            if np.array_equal(self.agent, goal):
                return True
            else:
                return False

    def update_utility(self, state: np.array, new_value: float):
        self.utilities[state[0] -1][state[1]-1] = new_value
        return self.utilities
        
    def update_agent(self, move: np.array):
        '''
        Update agent using an action. The input is a direction based on matrix
        notation of the board (up is -1, down is 1, right is 1, left is -1). The
        agent itself is updated and so is the board. This is meant to be used 
        when the action is decided and the move is *valid*!
        '''
        # board index starts at 0 -- agent index is logical matrix index (starts
        # at 1)
        old = self.agent
        self.board[old[0]-1][old[1]-1] = OPEN
        self.agent = old + move
        new = self.agent
        self.board[new[0] - 1][new[1] - 1] = AGENT
        return self.agent
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
            x = int(wall_squares[i]) - 1
            y = int(wall_squares[i+1]) - 1
            self.board[x][y] = WALL 
            self.walls.append(np.array([x, y]))

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
            self.boxes.append(np.array([x, y]))

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
            self.goals.append(np.array([x, y]))
    
    def _setup_agent(self, agent_info: str):
        '''
        Use the information in agent_info to initialize the agent into
        the board
        '''        
        agent_square = agent_info.split()
        agent_square = map(int,agent_square)
        x, y = agent_square
        self.board[x-1][y-1] = AGENT
        self.agent = np.array([x, y])
    
    def _setup_utilities(self) -> None:
        for m in range(self.num_rows):
            for n in range(self.num_cols):
                board_index = self.board[m][n]
                if board_index == WALL:
                    self.utilities[m][n] = np.nan
    
    def _setup_rewards(self) -> None:
        for m in range(self.num_rows):
            for n in range(self.num_cols):
                board_index = self.board[m][n]
                if board_index == OPEN or board_index == AGENT:
                    self.rewards[m][n] = -1
                elif board_index == GOAL:
                    self.rewards[m][n] = 1
                else:
                    self.rewards[m][n] = 0
                # if board_index == WALL:
                #     self.rewards[m][n] = 0
                # if board_index == BOX:
                #     self.rewards[m][n] = 0 # for now 

    # -------------------------------------------------------- #
    # -------------------------------------------------------- #