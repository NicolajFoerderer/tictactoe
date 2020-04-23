import random

import numpy as np


class Learner:
    """Learner class for applying the q-learning algorithm to our game of Tic Tac Toe.

    :param game: TicTacToe game instance
    :param learning_rate: The learning rate of the q-learning algorithm. Between 0 and 1.
    :param discount_factor: The discount factor of the q-learning algorithm. Between 0 and 1.

    Class instances:
        state_list: List of all explored states, represented as string
        q_table:    Table of Q values for each state-action pair
        old_state:  The state from the previous step
        old_action: The action from the previous step
    """
    state_list = []
    q_table = []
    old_state = None
    old_action = None

    def __init__(self, game, learning_rate=0.2, discount_factor=0.2):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.action_list = game.actions.flatten().tolist()

    def step(self, game, player_id):
        """One iteration of the q-learning algorithm.

        :param game: Current TicTacToe game instance
        :param player_id: The integer ID of the player
        :return: Action string with the highest expected future reward.
        """
        new_state = game.state

        # Check if new state has been explored before.
        if not self.is_state_in_list(new_state):
            self.state_list.append(str(new_state))
            self.q_table.append(self.init_q())

        # Get reward of new state
        reward = self.reward(game.check_win(), player_id)

        # Select action with max value
        new_action = self.valid_max_action(new_state)

        # Update old q, based on the new state and reward.
        if self.old_state is not None:
            self.update_q(self.old_state, new_state, self.old_action, reward)

        # Updates for next iteration.
        self.old_state = new_state.copy()
        self.old_action = new_action

        return new_action

    def reset(self):
        """Reset the instance for a new iteration of the algorithm.
        """
        self.old_state = None
        self.old_action = None

    def update_q(self, old_state, new_state, old_action, reward):
        """Update the q value for the state-action pair.

        Because we know the future state for our agent only after the opponent has
        played, we update the q-value from the old state retrospectively.

        :param old_state: The state from the previous iteration.
        :param new_state: The state from the current iteration.
        :param old_action: The action string from the previous iteration.
        :param reward: The reward for the current state (which is the result from the old action and state.)
        """
        self.q_table[self.state_index(old_state)][self.action_index(old_action)] = (
                self.q_table[self.state_index(old_state)][self.action_index(old_action)] + self.learning_rate * (
                reward + self.discount_factor * self.max_q(new_state)
                - self.q_table[self.state_index(old_state)][self.action_index(old_action)]))

    def get_random_action(self, game):
        """Get a random but valid action.

        :param game: Current TicTacToe game instance
        :return: Action string
        """
        try:
            return random.choice(game.valid_actions())
        except:
            return None

    def init_q(self):
        """Initialize a new row of q-values

        :return: list of initialized q-values
        """
        return [0] * len(self.action_list)

    def is_state_in_list(self, state):
        """Check if current state is in list of previously explored states.

        :param state: Current state
        :return: Boolean
        """
        return str(state) in self.state_list

    def state_index(self, state):
        """Get the index of a state in our state list

        :param state: State
        :return: Index
        """
        return self.state_list.index(str(state))

    def action_index(self, action):
        """Get the index of a action in our action list

        :param action: Action string
        :return: Index
        """
        return self.action_list.index(action)

    def reward(self, game_state, player_id):
        """Reward function for the q-learning algorithm

        :param game_state: The winning state of the game. Integer between -1 and 2
        :param player_id: The learners player ID
        :return: Reward, from -10 to 10
        """
        if game_state > 0:
            if game_state == player_id:
                return 10
            else:
                return -10
        else:
            return -1

    def max_q(self, state):
        """Get the maximum q-value of a state.

        :param state: State
        :return: Maximum q-value
        """
        return max(self.q_table[self.state_index(state)])

    def arg_max_q(self, state):
        """Get the index of the maximum q-value of a state.

        :param state: State
        :return: Index
        """
        return np.argmax(self.q_table[self.state_index(state)])

    def valid_max_action(self, state):
        """Get a valid action with the highest q-value.

        :param state: State
        :return: Action string
        """
        action_indices = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        action_indices_valid = action_indices[np.isnan(state)].tolist()
        valid_q = [self.q_table[self.state_index(state)][i] for i in action_indices_valid]

        if valid_q:
            max_ind = np.argwhere(valid_q == np.amax(valid_q))

            # If we have multiple maxima, select one randomly.
            if len(max_ind) > 1:
                max_ind = random.choice(max_ind)
            return self.action_list[action_indices_valid[int(max_ind)]]
        else:
            return None
