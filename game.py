from agents import MethodicalAgent, RandomAgent, MinimaxAgent


class Grid:
    def __init__(self, size: int = 8):
        self.size = size
        self.board = ['-'*size]*size
        self.black_disks = 0
        self.white_disks = 0
        self.empty_slots = size * size
        self.black_sign = 'X'
        self.white_sign = '0'
        self.initialize()

    def get_size(self):
        return self.size

    def get_board(self):
        return self.board

    def get_black_disks(self):
        return self.black_disks

    def get_white_disks(self):
        return self.white_disks

    def get_empty_slots(self):
        return self.empty_slots

    def total_disks(self):
        return self.black_disks + self.white_disks

    def initialize(self):
        # fix the board for the starting state
        pos = int(self.size/2)
        self.set_disk(pos - 1, pos - 1, self.black_sign)
        self.set_disk(pos, pos, self.black_sign)
        self.set_disk(pos - 1, pos, self.white_sign)
        self.set_disk(pos, pos - 1, self.white_sign)
        self.black_disks = 2
        self.white_disks = 2

    def copy_grid(self):
        # returns a deep copy of the grid
        grid = Grid(self.size)
        grid.board = [row[:] for row in self.board]
        grid.black_disks = self.black_disks
        grid.white_disks = self.white_disks
        grid.empty_slots = self.empty_slots
        return grid

    def __str__(self):
        string = ''
        for row in self.board:
            string += row + '\n'
        return string[:-1]

    def is_outside_board(self, row: int, col: int) -> bool:
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return True
        return False

    def set_disk(self, row: int, col: int, sign: str) -> None:
        # puts a disk on the board or replace one
        if self.is_outside_board(row, col):
            return
        # updating disks count
        if self.board[row][col] == '-':
            self.empty_slots -= 1
            if sign == self.black_sign:
                self.black_disks += 1
            else:
                self.white_disks += 1
        else:
            if sign == self.black_sign:
                self.black_disks += 1
                self.white_disks -= 1
            else:
                self.black_disks -= 1
                self.white_disks += 1

        self.board[row] = self.board[row][:col] + sign + self.board[row][col+1:]

    def set_disk_line(self, row: int, col: int, sign: str, x_step: int, y_step: int) -> None:
        x_to, y_to = row + x_step, col + y_step
        row, col = row + x_step, col + y_step
        # we look for the same disk sign of the direction provided by x_step and y_step
        while(not self.is_outside_board(x_to, y_to) and not self.board[x_to][y_to] == '-'
              and not self.board[x_to][y_to] == sign):
            x_to += x_step
            y_to += y_step
        # we didn't find any disks to replace
        if self.is_outside_board(x_to, y_to) or self.board[x_to][y_to] == '-':
            return
        # replace all the disks that have different sign
        while not(row == x_to and col == y_to):
            self.set_disk(row, col, sign)
            row += x_step
            col += y_step

    def set_disk_board(self, row: int, col: int, sign: str) -> None:
        # puts the disk on the board and fix other disk on the board by the game rules
        self.set_disk(row, col, sign)
        self.set_disk_line(row, col, sign, -1, -1)
        self.set_disk_line(row, col, sign, -1, 0)
        self.set_disk_line(row, col, sign, -1, +1)
        self.set_disk_line(row, col, sign, 0, -1)
        self.set_disk_line(row, col, sign, 0, +1)
        self.set_disk_line(row, col, sign, +1, -1)
        self.set_disk_line(row, col, sign, +1, 0)
        self.set_disk_line(row, col, sign, +1, +1)

    def connected(self, row: int, col: int) -> bool:
        # checks if the new disk we want to put is near another one

        if not self.is_outside_board(row - 1, col) and not self.board[row - 1][col] == '-':
            return True
        if not self.is_outside_board(row + 1, col) and not self.board[row + 1][col] == '-':
            return True
        if not self.is_outside_board(row, col - 1) and not self.board[row][col - 1] == '-':
            return True
        if not self.is_outside_board(row, col + 1) and not self.board[row][col + 1] == '-':
            return True
        return False


class Player:
    _num_of_players = 2

    def __init__(self, sign: str, agent='M'):
        self.sign = sign
        self.agent = self.get_agent(agent)
        self.player_num = self._num_of_players

    def get_sign(self):
        return self.sign

    def get_player_num(self):
        return self.player_num

    def get_players_num(self):
        return self._num_of_players

    def get_action(self, game_state):
        return self.agent.get_action(game_state)

    def get_agent(self, kind: str):
        if kind == 'R':
            return RandomAgent()
        elif kind == 'H1':
            return MinimaxAgent('H1')
        elif kind == 'H2':
            return MinimaxAgent('H2')
        else:  # kind == 'M'
            return MethodicalAgent()


class GameState:
    def __init__(self, grid=Grid(), player1=Player('X'), player2=Player('0'), state=0, player_turn=1):
        self.grid = grid
        self.player1 = player1
        self.player2 = player2
        self.state = state
        self.player_turn = player_turn
        self.prev_game_state = None

    def __str__(self):
        return str(self.grid)

    def get_turn_sign(self):
        if self.player_turn == 1:
            return self.player1.get_sign()
        else:
            return self.player2.get_sign()

    def get_legal_actions(self) -> list:
        if self.grid.get_empty_slots() == 0:
            return []
        list_actions = []
        grid = self.grid.get_board()
        # checks the whole board for a valid placement of a disk
        for row in range(self.grid.get_size()):
            for col in range(self.grid.get_size()):
                if grid[row][col] == '-' and self.grid.connected(row, col) and self.is_flip(row, col):
                    list_actions.append((row, col))

        return list_actions

    def generate_successor(self, action: tuple):
        if len(action) != 3:
            return

        row, col, sign = action
        grid = self.grid.copy_grid()
        next_turn = (self.player_turn % self.player1.get_players_num()) + 1
        next_game_state = GameState(grid, self.player1, self.player2, self.state + 1, next_turn)
        grid.set_disk_board(row, col, sign)

        return next_game_state

    def is_flip(self, row: int, col: int) -> bool:
        sign = self.get_turn_sign()
        next_state = self.generate_successor((row, col, sign))

        if sign == self.grid.black_sign and (self.grid.get_black_disks() + 1 < next_state.grid.get_black_disks()):
            return True
        elif sign == self.grid.white_sign and (self.grid.get_white_disks() + 1 < next_state.grid.get_white_disks()):
            return True
        else:
            return False

    def game_over(self) -> bool:
        return not self.get_legal_actions()
