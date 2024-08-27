import random


class MethodicalAgent:
    """
    An agent that will return a action
    The chosen move is based on the first available move
    """
    def get_action(self, game_state) -> tuple:
        legal_actions = game_state.get_legal_actions()
        row, col = legal_actions[0]
        sign = game_state.get_turn_sign()
        return row, col, sign


class RandomAgent:
    """
    An agent that will return an action
    The chosen move is based on the first available move
    """
    def get_action(self, game_state) -> tuple:
        legal_actions = game_state.get_legal_actions()
        legal_action = random.choice(legal_actions)
        row, col = legal_action
        sign = game_state.get_turn_sign()
        return row, col, sign


class MinimaxAgent:
    """
    An agent that will return an action
    The chosen move is based on the function evaluation
    """
    def __init__(self, function: str, depth=1):
        self.function = function
        self.depth = depth

    def get_action(self, game_state) -> tuple:
        sign = game_state.get_turn_sign()

        _, move = self.minimax_search(game_state, self.depth * game_state.player1.get_players_num())
        return move + (sign,)

    def h1(self, game_state):
        """
        We will use basic logic, the more black disks i have the better
        """
        return game_state.grid.get_black_disks()

    def h2(self, game_state):
        """
        We will use a strategy from Wikipedia.
        At the start of the game try to flip minimal amount of disks.
        We picked the first half as the start of the game.
        After the start of the game ended we will use the same tactic as H1.
        We will also check the corners, cause if you control them they cannot be flipped
        """
        grid, size = game_state.grid, game_state.grid.get_size()
        result, num_turns = 0, int((size*size)/2)
        prev_game_state = game_state.prev_game_state

        if grid.board[0][0] == grid.black_sign:
            result += size
        if grid.board[0][0] == grid.white_sign:
            result -= size
        if grid.board[0][size-1] == grid.black_sign:
            result += size
        if grid.board[0][size-1] == grid.white_sign:
            result -= size
        if grid.board[size-1][0] == grid.black_sign:
            result += size
        if grid.board[size-1][0] == grid.white_sign:
            result -= size
        if grid.board[size-1][size-1] == grid.black_sign:
            result += size
        if grid.board[size-1][size-1] == grid.white_sign:
            result -= size

        if prev_game_state is not None and game_state.state < num_turns:
            result += (size * size) - (game_state.grid.get_black_disks() - prev_game_state.grid.get_black_disks())
        else:
            result += game_state.grid.get_black_disks()

        return result

    def minimax_search(self, game_state, depth) -> tuple:
        """
        Minimax tree
        """
        if depth == 0 or game_state.game_over():
            if self.function == 'H1':
                return self.h1(game_state), None
            return self.h2(game_state), None  # self.function == 'H2'

        legal_actions, move = game_state.get_legal_actions(), None
        sign = game_state.get_turn_sign()
        children = [game_state.generate_successor(action + (sign,)) for action in legal_actions]

        if sign == game_state.grid.black_sign:  # 'X'
            cur_max = float('-inf')
            for index, child in enumerate(children):
                v, _ = self.minimax_search(child, depth - 1)
                if v > cur_max:
                    cur_max = v
                    move = legal_actions[index]
            return cur_max, move
        else:  # '0'
            cur_min = float('inf')
            for index, child in enumerate(children):
                v, _ = self.minimax_search(child, depth - 1)
                if v < cur_min:
                    cur_min = v
                    move = legal_actions[index]
            return cur_min, move
