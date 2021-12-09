from custom_errors import *
from sokoban import Sokoban
from global_constants import *
from type_hepler import *
from random import randint, uniform, choice
import printing


class QLearner(Sokoban):
    '''
    A class that defines the Q learning agent. This class inherits the Sokoban class, 
    meaning this Q-Learner is valid for the Sokoban game and inherits all the methods
    defined in the child class Sokoban.
    '''
    def __init__(self, path: str):

        # initialize the child class sokoban game which allows this class
        # to inherit all methods of the child class
        Sokoban.__init__(self, path)

        #--- for the q-learning method
        self._valid_states = self._get_valid_states()
        self.q_table = self._setup_q_table()
        self.frequency_table = self._setup_frequencies()
        self.epsilon = EPSILON
    
    def get_optimal_policy(self) -> np.array:
        '''
        Determine the optimal policy as defined by the determined q table
        '''

        self.initialize_gamestate()

        all_actions = []

        steps = 0
        while not self.is_terminal() and steps < MAX_STEPS_ALLOWED_FOR_OPTIMAL:

            # get maximum q value given a state index and get back
            # action index that has maximum q
            action_maximizing_q = self._exploit_action()

            all_actions.append(action_maximizing_q)

            # move the agent using action that maximizes q
            if self.is_valid_action(action_maximizing_q):
                self.take_action(action_maximizing_q)
            else:
                print('Agent keeps going to same place, probably did not find optimal')
                raise NotOptimalAction

            steps+=1

            if steps > MAX_STEPS_ALLOWED_FOR_OPTIMAL:
                print('There are too many steps, propably did not find optimal')
                raise NotOptimalAction
        
        return all_actions


    def observe_action(self, action: int) -> tuple[float, np.array]:
        '''
        Obseve what taking action a in state s would do. You observe the next state
        and the reward you would get for getting to that next state. The function 
        take_action() returns the result of the agents move which is either:
        OPEN:           moved to open space (not so good..)
        BOX:            moved a box to an open space (good!)
        BOX_ON_GOAL:    moved a box onto a goal (really good!)
        GOAL:           moved a box off a goal, so not it is in a goal space (bad!) 
        '''
        # only valid actions are allowed now....
        value_of_new_state = self.take_action(self.valid_actions[action])
        reward = self._determine_reward(value_of_new_state)
        new_state = self.agent 
        # if self.is_valid_action(action):
        #     value_of_new_state = self.take_action(action)
        #     reward = self._determine_reward(value_of_new_state)
        #     new_state = self.agent 
        # else:
        #     # if the action isn't valid the agent stays in the same place
        #     new_state = self.agent
        #     reward = self._determine_reward(NO_MOVE)
        return reward, new_state

    def epsilon_greedy(self) -> np.array:
        '''
        Determines an action based on the epsilon greedy method, where epsilon
        is constant
        '''
        # valid_actions = self.get_valid_actions()
        n = uniform(0,1)
        if n < self.epsilon:
            action = self._explore_action()
        else:
            action = self._exploit_action()
        return action

    def update_q_value(self, current_state: np.array, new_state: np.array,
                action: np.array, reward: float) -> None:
        '''
        The function that approximates the bellman update
        '''

        current_state_index = self._get_state_index(current_state)
        # action_index = self._get_action_index(action)
        action_index = action
        new_state_index = self._get_state_index(new_state)

        # increment frequency table
        self.frequency_table[current_state_index][action_index] += 1
        n_s_a = self.frequency_table[current_state_index, action_index]

        # get Q(s,a)
        q_s_a = self.q_table[current_state_index, action_index]
        # print(action_index)
        # get max a' Q(s', a')
        q_values_for_new_state = self._get_q_values(new_state_index)
        max_q_value = max(q_values_for_new_state.values())

        # for some reason the frequency table fucks everything up ?????
        # - it makes q values get insanely large
        # - oh im an idiot-- its because is should be alpha(n_s_a) where alpha is a 
        #   function lol
        # new_q_value = q_s_a + (ALPHA*n_s_a) * (reward + GAMMA * max_q_value - q_s_a)
        # with all this being said:
        # TODO:
        # create a function alpha(N[s,a]) to increment alpha based on the number
        # of times the agent has done a state action pair. this will help penalize
        # the agent for repeating the same actions

        # alpha = self.alpha_of_n(n_s_a)
        # new_q_value = q_s_a + (alpha) * (reward + GAMMA * max_q_value - q_s_a)
        new_q_value = q_s_a + (ALPHA) * (reward + GAMMA * max_q_value - q_s_a)

        if np.isnan(new_q_value) or np.isinf(new_q_value):
            pass
        elif new_q_value > PRECISION or new_q_value < -PRECISION:
            pass
            # raise ValuesTooBigError
        else:
            self.q_table[current_state_index][action_index] = new_q_value

    # -------------------------------------------------------- #
    # ----------- These are private methods! ----------------- #
    # -------------------------------------------------------- #

    # def max_q__s_prime_a_prime(self, current_state):
    #     possible_actions = [UP, DOWN, LEFT, RIGHT]
    #     for action in possible_actions:
    #         new_state = 
    #     pass

    def alpha_of_n(self, n) -> float:
        return 60/(120+n)

    def _determine_reward(self, value: BoardValue) -> float:
        '''
        Defines the rewards for if an agent moves to a board space that
        has one of the specified values -- or in the case of a box, its action
        either just moves a box, or puts it on a goal
        '''
        if value == OPEN:
            reward = MOVE_PENALTY
        elif value == BOX:
            reward = MOVE_BOX_REWARD
        elif value == GOAL:
            reward = MOVE_PENALTY
        elif value == BOX_ON_GOAL:
            reward = BOX_ON_GOAL_REWARD
        elif value == NO_MOVE:
            reward = MOVE_PENALTY
        elif value == ALL_BOXES_ON_GOAL:
            reward = SOLVE_GAME_REWARD
        elif value == DEADLOCK:
            reward = DEADLOCK_PENALTY
        return reward
    
    def _explore_action(self) -> np.array:
        '''
        returns an action chosen at random
        '''
        return self._get_random_action()
    
    def _exploit_action(self) -> np.array:
        '''
        returns an action by exploiting the q-table, although if the 
        entries are equivalent and max is irrelevant, an action is 
        chosen at random
        '''
        current_state = self.agent
        state_key = self._get_state_index(current_state)
        q_values = self._get_q_values(state_key)

        # valid_actions = self.valid_actions
        # first_action_index = self._get_action_index(valid_actions[0])
        valid_current_keys = list(self.valid_actions.keys())
        first_action_index = valid_current_keys[0]

        # if all the values are equal, exploiting is not possible
        if all(value == q_values[first_action_index] for value in q_values.values()):
            return self._get_random_action()
        else:
            max_key = max(q_values, key=q_values.get)
            # print('q vals', q_values)
            # print('max:', max_key)
            # return self.valid_actions[max_key]
            return max_key
        
    def _get_q_values(self, state_index: int) -> dict:
        '''
        returns a dictionary of the actions as keys and the approximated
        q values as values for a specific state index
        '''
        # valid_actions = self.valid_actions
        q_table = self.q_table
        q_value_dict = {}
        for action_key in self.valid_actions:
            # action_index = self._get_action_index(action)
            q_value_dict[action_key] = q_table[state_index][action_key]
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
        
    def _get_state_index(self, state: np.array) -> int:
        '''
        get state key index
        '''
        valid_states = self._valid_states
        for key in valid_states:
            if np.array_equal(state, valid_states[key]):
                return key

    def _get_random_action(self):
        '''
        choose a random action - numbered 1 through 4 where 1 = up, 2 = down,
        3 = left, 4 = right
        '''
        # valid_actions = self.valid_actions
        # action_indices = []
        # for action in valid_actions:
        #     action_index = self._get_action_index(action)
        #     action_indices.append(action_index)
        # value = choice(list(action_indices)
        # action = self._return_action_given_key(value)
        action = choice(list(self.valid_actions.keys()))
        # return self.valid_actions[action]
        return action

    def _return_action_given_key(self, action_index: int) -> np.array:
        '''
        return the action given the key index where 1 = up, 2 = down,
        3 = left, 4 = right
        '''
        if action_index == 1:
            return UP
        elif action_index == 2:
            return DOWN
        elif action_index == 3:
            return RIGHT
        elif action_index == 4:
            return LEFT
        elif action_index == 5:
            return BOX_UP
        elif action_index == 6:
            return BOX_DOWN
        elif action_index == 7:
            return BOX_RIGHT 
        elif action_index == 8:
            return BOX_LEFT

    def _get_action_index(self, action: np.array) -> int:
        '''
        Return the integer index for a given action which is an np.array
        '''
        if np.array_equal(action, UP):
            return 1
        elif np.array_equal(action, DOWN):
            return 2
        elif np.array_equal(action, LEFT):
            return 3 
        elif np.array_equal(action, RIGHT):
            return 4
        elif np.array_equal(action, BOX_RIGHT):
            return 5
        elif np.array_equal(action, BOX_DOWN):
            return 6
        elif np.array_equal(action, BOX_LEFT):
            return 7 
        elif np.array_equal(action, BOX_RIGHT):
            return 8
    # -------------------------------------------------------- #
    # -------------------------------------------------------- #

    # -------------------------------------------------------- #
    # ------ These are methods for initialization! ----------- #
    # -------------------------------------------------------- #
    def _setup_q_table(self) -> np.array:
        '''
        Setup the Q-Table:
        The states are indexed 1:number_of_states
        The actions are indexed 1:4, Up, Down Left, Right
        - np arrays must be numbers, although the state 1 refers to a place on the 
          board that is stored in the valid states dictionary
        0     1   2   3   4
        s_1   _   _   _   _
        s_2   _   _   _   _
        .     _   _   _   _
        s_n   _   _   _   _
        '''
        num_valid_states = len(self._valid_states)
        num_valid_actions = 8
        q_table = np.zeros(shape=(num_valid_states+1, num_valid_actions+1), dtype=float)

        # fill in the valid states in the first column, these are just ids
        for i in range(1, num_valid_states + 1):
            q_table[i][0] = i
        for j in range(num_valid_actions + 1):
            q_table[0][j] = j
        return q_table

    def _setup_frequencies(self) -> np.array:
        '''
        same as q-table
        '''
        num_valid_states = len(self._valid_states)
        num_valid_actions = 8
        frequency_table = np.zeros(shape=(num_valid_states+1, num_valid_actions+1), dtype=int)

        # fill in the valid states in the first column, these are just ids
        for i in range(1, num_valid_states + 1):
            frequency_table[i][0] = i
        for j in range(num_valid_actions + 1):
            frequency_table[0][j] = j
        return frequency_table