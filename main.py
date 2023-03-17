import tkinter as tk
import numpy as np
import random as rd


class Case:
    def __init__(self):
        self.is_flagged = False
        self.is_revealed = False
        self.is_bomb = False
        self.value = 0


#   size : (x, y)
class Board:
    def __init__(self, bombs, size):
        self.size = size
        self.board = np.array([[Case() for x in range(size[1])] for y in range(size[0])])
        self.bombs = bombs

    def create_board(self):
        fl_board = self.board.flatten()

        if (self.bombs >= len(fl_board)):
            return False

        for i in range(self.bombs):
            fl_board[i].is_bomb = True

        rd.shuffle(fl_board)

        self.board = np.reshape(fl_board, self.size)
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                self._assign_value(y, x)

    def _assign_value(self, y, x):
        board = self.board
        if (board[y][x].is_bomb is True):
            return

        print(f'Nos valeures initiales: {y}, {x}')
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if (dx == 0 and dy == 0):
                    continue

                if ((y + dy) >= self.size[0] or (x + dx) >= self.size[1]):
                    continue

                if ((y + dy) <= -1 or (x + dx) <= -1):
                    continue

                if (board[y + dy][x + dx].is_bomb is True):
                    board[y][x].value += 1

    def update_case(self, case, action):
        return

    def show_board(self):
        board = self.board
        for row in board:
            for case in row:
                print(f'{case.is_bomb},{case.value}', end='  |  ')
            print('\n')
        return


board = Board(9, (6, 6))
print(board.create_board())
board.show_board()
