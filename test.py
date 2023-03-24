from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import Qt

class MyButton(QPushButton):
    def __init__(self, parent=None):
        super(MyButton, self).__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('Left button clicked')
        elif event.button() == Qt.RightButton:
            print('Right button clicked')

if __name__ == '__main__':
    app = QApplication([])
    button = MyButton('Click me')
    button.show()
    app.exec_()
