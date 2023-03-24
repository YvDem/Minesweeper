import sys
import PyQt5.QtWidgets as wi
from PyQt5.QtCore import Qt
import PyQt5.QtGui as gu
import random as rd
sys.setrecursionlimit(10000)

class Color(wi.QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        self.c_palette = self.palette()
        self.c_palette.setColor(gu.QPalette.Window, gu.QColor(color))
        self.setPalette(self.c_palette)


class m_Button(wi.QPushButton):
    def __init__(self, text, y, x):
        super(m_Button, self).__init__(text)
        self.content = 0
        self.revealed = False
        self.y = y
        self.x = x

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('Left button clicked')
        elif event.button() == Qt.RightButton:
            print('Right button clicked')

    def get_content(self):
        return self.content
    
    def is_revealed(self):
        return self.revealed

class FenetrePrincipale(wi.QMainWindow):
    def __init__(self, x, y, b):
        super().__init__()
        self.x = x
        self.y = y
        self.setFixedSize(y * 25, x * 25)
        self.setWindowTitle('Minesweeper')
        self.layout = wi.QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        for dy in range(y):
            for dx in range(x):
                button = m_Button('', dy, dx)
                button.clicked.connect(self._afficher_value)
                button.setFixedSize(25, 25) 
                button.setFont(gu.QFont('Arial', 6))
                button.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                self.layout.addWidget(button, dy, dx)
        self._assign_value(x, y, b)
        self.widget = wi.QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def _get_all_bombs_pos(self, x, y, b):
        all_pos = []
        for dy in range(y):
            for dx in range(x):
                all_pos.append((dy, dx))
        bomb_pos = rd.sample(all_pos, b)
        return bomb_pos
    
    def _assign_value(self, x, y, b):
        bomb_pos = self._get_all_bombs_pos(x, y, b)
        for dy in range(y):
            for dx in range(x):
                case = self.layout.itemAtPosition(dy, dx).widget()
                if (dy, dx) in bomb_pos:
                    case.content = -1

        for dy in range(y):
            for dx in range(x):
                case = self.layout.itemAtPosition(dy, dx).widget()
                if case.get_content() == -1:
                    continue
        
                for ddy in range(-1, 2):
                    for ddx in range(-1, 2):
                        if (ddx == 0 and ddy == 0):
                            continue

                        if ((dx + ddx) >= x or (dy + ddy) >= y):
                            continue

                        if ((dy + ddy) <= -1 or (dx + ddx) <= -1):
                            continue

                        a_case = self.layout.itemAtPosition(dy + ddy, dx + ddx).widget()
                        if (a_case.get_content() == -1):
                            case.content += 1
    
    def _update_around_values(self, y, x):
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy == 0 and dx == 0:
                    continue

                new_y = y + dy
                new_x = x + dx

                if (new_y < 0 or new_y >= self.y or new_x < 0 or new_x >= self.x):
                    continue

                case = self.layout.itemAtPosition(new_y, new_x).widget()
                if case.is_revealed():
                    continue

                case.revealed = True
                case.setStyleSheet("background-color: #afeaed")
                if case.get_content() == 0:
                    self._update_around_values(new_y, new_x)
                else:
                    case.setText(str(case.get_content()))
    
    def _afficher_value(self):
        value = self.sender().get_content()
        x = self.sender().x
        y = self.sender().y
        text = value
        if value == 0:
            self._update_around_values(y, x)
            text = ''
        if value == -1:
            self.popup = wi.QMessageBox(wi.QMessageBox.Information, 'Message', 'PERDU!!!!')
            self.popup.show()
        self.sender().setText(str(text))
        self.sender().setStyleSheet("background-color: #afeaed")

app = wi.QApplication([])
if app is None:
    app = wi.QApplication(sys.argv)

window = FenetrePrincipale(25, 25, 100)
window.show()
app.exec_()