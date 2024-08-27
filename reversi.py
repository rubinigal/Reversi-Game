import argparse
import sys
import time

from game import Grid, Player, GameState


class Game:
    def __init__(self, player1='M', player2='M'):
        self.player1 = Player('X', player1)
        self.player2 = Player('0', player2)
        self.game_state = GameState(Grid(), self.player1, self.player2)

    def game_over(self) -> bool:
        return self.game_state.game_over()

    def next_action(self):
        if self.game_state.player_turn == 1:
            action = self.player1.get_action(self.game_state)
        else:
            action = self.player2.get_action(self.game_state)
        return action

    def next_turn(self, action):
        if len(action) != 3:
            return
        prev_game_state = self.game_state
        self.game_state = self.game_state.generate_successor(action)
        self.game_state.prev_game_state = prev_game_state

    def display(self, action: tuple):
        if len(action) != 3:
            return

        row, col, sign = action
        new_grid = self.game_state.generate_successor(action).grid
        num_black, num_white = new_grid.get_black_disks(), new_grid.get_white_disks()
        if sign == self.player1.sign:
            player_num = 1
        else:
            player_num = 2

        print('State ' + str(self.game_state.state))
        print(self.game_state)
        print(f'State {self.game_state.state + 1}, Player {player_num} moved,'
              f' Action: put {sign} on position ({row}, {col})')
        print(new_grid)
        print(f'Result - Player 1: {num_black} disks, Player 2: {num_white} disks, Total: {num_black+num_white} disks')

    def display_all(self):
        legal_moves = self.game_state.get_legal_actions()
        sign = self.game_state.get_turn_sign()

        for move in legal_moves:
            row, col = move
            self.display((row, col, sign))

    def set_players_depth(self, depth=1):
        try:
            self.player1.agent.depth = depth
            self.player2.agent.depth = depth
        finally:
            pass


def read_command(argv: list) -> dict:
    """
    Processes the command used to run reversi from the command line.
    """
    parser = argparse.ArgumentParser(description='Reversi Game Options')

    parser.add_argument('-p', type=int, default=0, dest='play_turn', help='Control the amount of turns displayed')
    parser.add_argument('-t', type=int, default=0, dest='pause_time', help='Control the time flow of turns')
    parser.add_argument('-displayAllActions', type=int, default=-1, dest='display_all_actions',
                        help='Display all actions from one state')
    parser.add_argument('-methodical', type=int, default=-1, dest='methodical',
                        help='Showcase the first n turns using methodical agents')
    parser.add_argument('-random', type=int, default=-1, dest='random',
                        help='Showcase the first n turns using random agents')
    parser.add_argument('first_function', nargs='?', choices=['H1', 'H2'], help="First function: 'H1' or 'H2'")
    parser.add_argument('second_function', nargs='?', choices=['H1', 'H2'], help="Second function: 'H1' or 'H2'")
    parser.add_argument('-ahead', type=int, default=1, dest='ahead', help='Choose the depth of the minimax tree')

    options = parser.parse_args(argv)
    other = options._get_args()  # Get any additional arguments
    if len(other) != 0:
        raise Exception('Command line input not understood: ' + str(other))
    args = dict()

    args['pause_time'] = options.pause_time
    args['play_turn'] = options.play_turn
    args['display_all_actions'] = options.display_all_actions
    args['methodical'] = options.methodical
    args['random'] = options.random
    args['first_function'] = options.first_function
    args['second_function'] = options.second_function
    if options.ahead > 0:
        args['ahead'] = options.ahead
    else:
        args['ahead'] = 1

    return args


def run_game(pause_time: int, play_turn: int, display_all_actions: int, methodical: int, random: int,
             first_function: str, second_function: str, ahead: int):
    """
    Here we control the flow of the game
    :param pause_time: time between turns in sec
    :param play_turn: how many turns to show to screen from the first turn
    :param display_all_actions: in witch turn to show all available action for player
    :param methodical: agents will play by the first action provided
    :param random: agents will play by the random action provided
    :param first_function: agents will play based on evaluation function
    :param second_function: second agent will play based on evaluation function
    :param ahead: choose the depth of the minimax tree
    :return: None
    """
    # Starts the game based on the different kinds of agents
    if methodical >= 0:
        game = Game('M', 'M')
    elif random >= 0:
        game = Game('R', 'R')
    elif second_function is not None:
        game = Game(first_function, second_function)
    elif first_function is not None:
        game = Game(first_function, first_function)
        game.set_players_depth(ahead)
    else:
        game = Game()

    num_disks = game.game_state.grid.total_disks()
    while not game.game_over():  # Game flow
        action = game.next_action()

        if num_disks == display_all_actions:  # Command -displayAllActions
            game.display_all()
            break  # We can use break here or not depends on if we want the game to end or not

        if methodical > 0 or random > 0:
            # First part of command -methodical, -random (first n turns to display)
            game.display(action)
            methodical -= 1
            random -= 1

        if pause_time > 0:  # Command -t (command for testing)
            time.sleep(pause_time)

        if play_turn > 0:  # Show every turn till n (command for testing)
            print(game.game_state.grid)
            print()
            play_turn -= 1

        game.next_turn(action)  # Controls the game progress (by one turn)
        num_disks = game.game_state.grid.total_disks()  # Command -displayAllActions

    if game.game_over():
        black, white = game.game_state.grid.get_black_disks(), game.game_state.grid.get_white_disks()
        print('Game ended')
        print(game.game_state.grid)
        if black > white:
            print(f'Black player won with {black} black disks to {white} white disk')
        else:
            print(f'White player won with {white} white disks to {black} black disk')

    # Wait for the user to press any key before exiting
    input("Press any key to exit...")


if __name__ == '__main__':
    args = read_command(sys.argv[1:])
    run_game(**args)
    pass
