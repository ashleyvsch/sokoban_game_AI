import sokoban_structures
from global_constants import *
import helper
import printing
from type_hepler import SokobanGame
from random import randint


class QLearner:
    def __init__(self, gamestate: SokobanGame):
        self._gamestate = gamestate

        #--- for the q-learning method
        self._valid_states = self._get_valid_states()
        self.q_table = self._setup_q_table()
        self.frequency_table = self._setup_frequencies()

    ### TODO:
    ### explore/exploit return an action, the movement will be determined 
    ### later dependent on if the action is valid, but the q-table 
    ### needs to be updated for that action chosen regardless if the 
    ### action results in the same state
    
    def explore_action(self) -> np.array:
        '''
        returns an action chosen at random
        '''
        return self._get_random_action()
    
    def exploit_action(self) -> np.array:
        '''
        returns an action by exploiting the q-table, although if the 
        entries are equivalent and max is irrelevant, an action is 
        chosen at random
        '''
        current_state = self._gamestate.agent
        state_key = self._get_key_index(current_state)
        q_values = self._get_q_values(state_key)

        # if all the values are equal, exploiting is not possible
        if all(value == q_values[1] for value in q_values.values()):
            return self._get_random_action
        else:
            max_key = max(q_values, key=q_values.get)
            return self._return_action_given_key(max_key)
        
        # # make sure the chosen action is really valid, then return it,
        # # if not, the action just stays
        # if self._gamestate.is_valid_action(action):
        #     return action
        # else: 
        #     return STAY
        
    def _get_q_values(self, index) -> dict:
        q_table = self.q_table
        q_value_dict = {}
        for i in range(1,5):
            q_value_dict[i] = q_table[index][i]
        return q_value_dict

    def _get_valid_states(self) -> list:
        ''' 
        determines how many states are valid for the agent to move, 
        which is really anything besides a wall and invalid space
        '''
        board = self.board
        num_rows = self.num_rows
        num_cols = self.num_cols
        valid_states = {}
        index = 1
        for m in range(num_rows):
            for n in range(num_cols):
                if board[m][n] != WALL and board[m][n] != INVALID:
                    valid_states[index]  = np.array([m, n])
                    index += 1
        return valid_states
        
    def _setup_q_table(self) -> np.array:
        '''
        setup the q-table
        '''
        num_valid_states = len(self._valid_states)
        num_valid_actions = 4
        q_table = np.zeros(shape=(num_valid_states+1, num_valid_actions+1), dtype=float)

        # fill in the valid states in the first column, these are just ids
        for i in range(1, num_valid_states + 1):
            q_table[i][0] = i
        for j in range(num_valid_actions + 1):
            q_table[0][j] = j
        return q_table

    def _setup_frequencies(self) -> np.array:
        num_valid_states = len(self._valid_states)
        num_valid_actions = 4
        frequency_table = np.zeros(shape=(num_valid_states+1, num_valid_actions+1), dtype=int)

        # fill in the valid states in the first column, these are just ids
        for i in range(1, num_valid_states + 1):
            frequency_table[i][0] = i
        for j in range(num_valid_actions + 1):
            frequency_table[0][j] = j
        return frequency_table

    def _get_key_index(self, state: np.array) -> int:
        valid_states = self._gamestate._valid_states
        for key in valid_states:
            if np.array_equal(state, valid_states[key]):
                return key

    def _get_random_action(self) -> 'action':
        value = randint(1, 4)
        return self._return_action_given_key(value)

    def _return_action_given_key(self, value) -> np.array:
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


if __name__ == '__main__':
    building()