import sys
import PyQt5.QtWidgets as wi
from PyQt5.QtCore import QCoreApplication
import PyQt5.QtGui as gu
import random as rd

class Color(wi.QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        self.c_palette = self.palette()
        self.c_palette.setColor(gu.QPalette.Window, gu.QColor(color))
        self.setPalette(self.c_palette)


class m_Button(wi.QPushButton):
    def __init__(self, text):
        super().__init__()
        wi.QPushButton.__init__(self, text)
        self.content = 0
        self.revealed = False

    def get_content(self):
        return self.content
    
    def is_revealed(self):
        return self.revealed

class FenetrePrincipale(wi.QMainWindow):
    def __init__(self, x, y, b):
        super().__init__()
        self.x = x
        self.y = y
        self.setFixedSize(y * 40, x * 40)
        self.setWindowTitle('Minesweeper')
        self.layout = wi.QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        for dy in range(y):
            for dx in range(x):
                button = m_Button('')
                button.clicked.connect(self._afficher_value)
                button.setFixedSize(40, 40) 
                button.setFont(gu.QFont('Arial', 8)) 
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

    
    def _afficher_value(self):
        value = self.sender().get_content()
        self.sender().setText(str(value))

app = QCoreApplication.instance()
if app is None:
    app = wi.QApplication(sys.argv)

window = FenetrePrincipale(20, 20, 401)
window.show()
app.exec_()