"""
With this example script, we let a learning agent play
against a random player for N_ROUNDS*N_GAMES games.
After that, you can play against the trained agent.
"""

from collections import Counter

from tictactoe.learner import Learner
from tictactoe.player import Player
from tictactoe.tic_tac_toe import TicTacToe

LEARNING_RATE = 0.5
DISCOUNT_FACTOR = 0.4
N_GAMES = 500  # Games per round
N_ROUNDS = 10  # Total rounds of training


def one_round_of_training(game):
    """Playing N_GAMES games which counts as one round of training.

    :param game: An instance of the TicTacToe class.
    :return: List of game results.
    """
    wins = []
    for _ in range(N_GAMES):
        game.start()
        wins.append(game.winner)
    return wins


def print_winner_stats(winning_history):
    """Display the winning rates of both players.

    :param winning_history: List of game results.
    """
    counter = Counter(winning_history)
    p1_win = 100 * counter[1.0] / sum(counter.values())
    p2_win = 100 * counter[2.0] / sum(counter.values())
    print('Player 1 Wins:', p1_win, '%')
    print('Player 2 Wins:', p2_win, '%')


if __name__ == '__main__':
    # Create an instance of a Tic Tac Toe game.
    game = TicTacToe()

    # The learner object is used to initialize a learning player.
    # Note: Player one will always start the game.
    learner = Learner(game, learning_rate=LEARNING_RATE, discount_factor=DISCOUNT_FACTOR)
    game.p1 = Player(id=1, type='learner', learner=learner)

    # Let the learning player play against a random player.
    game.p2 = Player(id=2, type='random')

    # Play N_ROUNDS rounds of N_GAMES games and print the progress of the winning rate.
    for i in range(N_ROUNDS):
        print('Round', i + 1)
        winning_history = one_round_of_training(game)
        print_winner_stats(winning_history)

    # Let the trained agent play against a human player.
    game.p2.type = 'human'
    while True:
        game.start()
