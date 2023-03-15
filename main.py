import tkinter as tk
import numpy as np
import random as rd


class Case:
    def __init__(self):
        self.is_flagged = False
        self.is_revealed = False
        self.is_bomb = False
        self.value = 0
        self.x = None
        self.y = None


#   size : (x, y)
class Board:
    def __init__(self, bombs, size):
        self.size = size
        self.board = np.full((size[0], size[1]), Case())
        self.bombs = bombs


    def create_board(self):
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                self.board[i][j].x = j
                self.board[i][j].y = i
        flat_board = self.board.flatten()

        bombs = 0
        for case in flat_board:
            rand = rd.randint(0, bombs)
            if (rand == 1):
                bombs += 1
                case.is_bomb = True
        for case in flat_board:
            self._assign_value(self.board, case)

    def _assign_value(self, board, case):
        if (case.is_bomb is True):
            return
        

    def update_case(self, case, action):
        return

    def show_board(self):
        return

board = Board(5, (4, 4))
print(board.create_board())
