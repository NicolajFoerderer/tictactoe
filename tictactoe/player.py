import random


class Player:
    """Player class to play a game of Tic Tac Toe.

    :param id: The integer ID of the new player
    :param type: Type of the player. Available types are 'human', 'random' and 'learner'
    :param learner: If type is 'learner' we have to pass a Learner object.
    """
    def __init__(self, id, type, learner=None):
        self.id = id
        self.type = type
        self.learner = learner

    def get_action(self, game):
        """Get decision for an action corresponding to the type of player.

        :param game: Current TicTacToe game instance
        :return: Selected action string
        """
        if self.type == 'human':
            game.print_state()
            return self.ask_for_action(game)
        if self.type == 'random':
            return self.get_random_action(game)
        if self.type == 'learner':
            return self.learner.step(game, self.id)

    def get_random_action(self, game):
        """Get a random but valid action. If board is full, return nothing.

        :param game: Current TicTacToe game instance
        :return: Selected action string
        """
        try:
            return random.choice(game.valid_actions())
        except:
            return None

    def ask_for_action(self, game):
        """Ask human player for input.

        :param game: Current TicTacToe game instance
        :return: Selected action string
        """
        answer = input("Action for player " + str(self.id) + "? (Type ? for help)\n")

        if answer in game.valid_actions():
            return answer
        elif answer == '?':
            print('Valid actions are:', '%s' % ', '.join(map(str, game.valid_actions())))
            return self.ask_for_action(game)
        else:
            print('Please enter a valid action:', '%s' % ', '.join(map(str, game.valid_actions())))
            return self.ask_for_action(game)
