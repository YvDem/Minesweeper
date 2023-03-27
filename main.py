import sys
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QGridLayout, QMessageBox
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
import random as rd
sys.setrecursionlimit(10000)

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        self.c_palette = self.palette()
        self.c_palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(self.c_palette)

class MnBoard():
    def __init__(self, size, bombs, signal):
        self.c = signal
        self.board = []
        self.board_size = size
        self.bombs = bombs
    
    def initBoard(self):
        bomb_pos = self._get_all_bombs_pos(self.board_size[0], self.board_size[1], self.bombs)
        for x in range(self.board_size[0]):
            self.board.append([])
            for y in range(self.board_size[1]):
                button = MnButton(x, y, self.c, '')
                if (x, y) in bomb_pos:
                    button.content = -1
                self.board[x].append(button)
        self._assign_value(self.board_size[0], self.board_size[1])
    
    def _get_all_bombs_pos(self, x, y, b):
        all_pos = []
        for dx in range(x):
            for dy in range(y):
                all_pos.append((dx, dy))
        bomb_pos = rd.sample(all_pos, b)
        return bomb_pos

    def _assign_value(self, x, y):
        for dx in range(x):
            for dy in range(y):
                case = self.board[dx][dy]
                if case.get_content() == -1:
                    continue
        
                for ddx in range(-1, 2):
                    for ddy in range(-1, 2):
                        if (ddx == 0 and ddy == 0):
                            continue

                        if ((dx + ddx) >= x or (dy + ddy) >= y):
                            continue

                        if ((dy + ddy) <= -1 or (dx + ddx) <= -1):
                            continue

                        a_case = self.board[dx + ddx][dy + ddy]
                        if (a_case.get_content() == -1):
                            case.content += 1

class Signals(QObject):
    leftClic = pyqtSignal(tuple)
    rightClic = pyqtSignal(tuple) 

class MnButton(QPushButton):
    def __init__(self, x, y, signal, txt):
        super().__init__(txt)
        self.c = signal
        self.content = 0
        self.revealed = False
        self.flagged = False
        self.y = y
        self.x = x
    
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.c.leftClic.emit(self.get_position())
        if (event.button() == Qt.RightButton):
            self.c.rightClic.emit(self.get_position())
    
    def get_content(self):
        return self.content
    
    def is_revealed(self):
        return self.revealed
    
    def get_position(self):
        return (self.x, self.y)
    
    def is_flagged(self):
        return self.flagged

class Fenetre(QMainWindow):
    def __init__(self, x, y, b):
        super().__init__()
        self.x = x
        self.y = y
        self.bombs = b
        self.initUI()

    def initUI(self):

        self.c = Signals()
        self.c.leftClic.connect(self.clickLeftButton)
        self.c.rightClic.connect(self.clickRightButton)

        board = MnBoard((self.x, self.y), self.bombs, self.c)
        board.initBoard()
        self.layout = QGridLayout()

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle("My App")
        for i, row in enumerate(board.board):
            for j, button in enumerate(row):
                button.setFixedSize(25, 25)
                button.setFont(QFont('Arial', 6))
                button.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                self.layout.addWidget(button, i, j)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        # we connect to the first button, since all button return the same signal class 
        self.setFixedSize(self.y * 25, self.x * 25)
        self.setWindowTitle('Minesweeper')
        self.show()

    def _flag_case(self, x, y):
        case = self.layout.itemAtPosition(x, y).widget()
        if(case.is_revealed()):
            return
        if(case.is_flagged()):
            case.flagged = False
            case.setIcon(QIcon())
            return
        else:
            case.flagged = True
            case.setIcon(QIcon('flag.png'))
    
    def _update_around_values(self, x, y):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dy == 0 and dx == 0:
                    continue

                new_y = y + dy
                new_x = x + dx

                if (new_y < 0 or new_y >= self.y or new_x < 0 or new_x >= self.x):
                    continue

                case = self.layout.itemAtPosition(new_x, new_y).widget()
                if case.is_revealed():
                    continue
                if case.get_content() == -1:
                    continue
                if case.is_flagged():
                    continue

                case.revealed = True
                case.setStyleSheet("background-color: #afeaed")
                if case.get_content() == 0:
                    self._update_around_values(new_x, new_y)
                else:
                    case.setText(str(case.get_content()))

    def _afficher_value(self, x, y):
        case = self.layout.itemAtPosition(x, y).widget()
        if case.is_flagged():
            return
        value = case.get_content()
        text = value
        if value == 0:
            self._update_around_values(x, y)
            text = ''
        if value == -1:
            self.popup = QMessageBox(QMessageBox.Information, 'Message', 'PERDU!!!!')
            self.popup.show()
        case.setText(str(text))
        case.setStyleSheet("background-color: #afeaed")

    def clickRightButton(self, position):
        self._flag_case(position[0], position[1])

    def clickLeftButton(self, position):
        self._afficher_value(position[0], position[1])
        

    
def main():
    app = QApplication(sys.argv)
    ex = Fenetre(25, 25, 100)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()