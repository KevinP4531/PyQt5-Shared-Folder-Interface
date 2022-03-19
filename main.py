import socket
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle("Hello World")
        self.show()

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())