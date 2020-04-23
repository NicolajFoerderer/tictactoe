import numpy as np


class TicTacToe:
    """Class for playing a game of Tic Tac Toe.

    :param p1:      player one, object of Player class
    :param p2:      player two, object of Player class

    Class instances:
        winner:     -1 = no winner, 0 = tie, 1 = p1 wins, 2 = p2 wins
        state:      3x3 matrix representing the board
        actions:    3x3 matrix representing the possible actions on the board
    """
    winner = -1
    state = np.empty((3, 3,))
    state[:] = np.nan
    actions = np.array([['NW', 'N', 'NE'],
                        ['W', 'C', 'E'],
                        ['SW', 'S', 'SE']])

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def start(self):
        """Start a game of Tic Tac Toe.
        """
        self.reset_game()
        step = 0
        while self.winner < 0:
            if step % 2 == 0:
                self.apply_action(self.p1.get_action(self), self.p1.id)
            else:
                self.apply_action(self.p2.get_action(self), self.p2.id)

            # Check game state for winners
            self.winner = self.check_win()

            if self.winner >= 0:
                if self.p1.type == 'human' or self.p2.type == 'human':
                    self.print_state()
                    self.print_winner()

                # To update the q-table for the last step, we have to
                # run the get_action function again for a last time.
                if self.p1.type == 'learner':
                    self.p1.get_action(self)
                elif self.p2.type == 'learner':
                    self.p2.get_action(self)

            step += 1

    def reset_game(self):
        """Reset the winner state, the game state (board) and the learner object if necessary.
        """
        self.winner = -1
        self.state[:] = np.nan
        if self.p1.type == 'learner':
            self.p1.learner.reset()
        elif self.p2.type == 'learner':
            self.p2.learner.reset()

    def apply_action(self, action, player_id):
        """Apply an action to the current state.

        :param action: Action string
        :param player_id: The players ID who does the move
        """
        self.state[self.actions == action] = player_id

    def valid_actions(self):
        """Actions that are allowed with the current state.

        :return: List of valid action strings.
        """
        return list(self.actions[np.isnan(self.state)])

    def check_win(self):
        """Function that checks if a player has won the game.

        :return: Winner state where:    -1 = no winner
                                        0 = draw
                                        i = player i wins
        """
        # Check rows for triple.
        for i in range(self.state.shape[0]):
            if not np.isnan(self.state[i, 0]):
                if self.state[i, 0] == self.state[i, 1] == self.state[i, 2]:
                    return self.state[i, 0]

        # Check columns for triple.
        for i in range(self.state.shape[1]):
            if not np.isnan(self.state[0, i]):
                if self.state[0, i] == self.state[1, i] == self.state[2, i]:
                    return self.state[0, i]

        # Check diagonal for triple.
        if not np.isnan(self.state[0, 0]):
            if self.state[0, 0] == self.state[1, 1] == self.state[2, 2]:
                return self.state[0, 0]
        if not np.isnan(self.state[2, 0]):
            if self.state[2, 0] == self.state[1, 1] == self.state[0, 2]:
                return self.state[2, 0]

        if not np.isnan(self.state).any():
            # Tie
            return 0
        else:
            # No winner
            return -1

    def print_winner(self):
        """Print winning message.
        """
        if self.winner >= 0:
            if self.winner == 0:
                print('Tie')
            else:
                print('Player', int(self.winner), 'wins \U0001F389')

    def print_state(self):
        """Print the current state (board) in a pleasant way.
        """
        print('\n')
        shape = self.state.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                self.print_value(self.state[i, j])
                if j < shape[1] - 1:
                    print('|', end='')
            if i < shape[0] - 1:
                print('\n – + – + – ')
        print('\n')

    def print_value(self, value):
        """Helper function to print values centered in the fields of the board.

        :param value: Content of a particular field of the board.
        """
        if not np.isnan(value):
            string = ' ' + str(int(value)) + ' '
            print(string, end='')
        else:
            print('   ', end='')
