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
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self._assign_value(x, y)

    def _assign_value(self, x, y):
        board = self.board
        if (board[x][y].is_bomb is True):
            return
        
        
        

    def update_case(self, case, action):
        return

    def show_board(self):
        flat_board = self.board.flatten()
        for elem in flat_board:
            print(f'{elem.is_flagged}, {elem.is_revealed}, {elem.is_bomb}, {elem.value}')
        return


board = Board(5, (4, 4))
print(board.create_board())
board.show_board()
