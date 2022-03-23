import socket
import sys
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QGridLayout, QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def connect(self):
        print("CONNECT")

    def upload(self):
        print("UPLOAD")

    def download(self):
        print("DOWNLOAD")

    def delete(self):
        print("DELETE")
    
    def dir(self):
        print("LIST DIR")

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        cnct_btn = QPushButton('CONNECT', self)
        cnct_btn.setToolTip('Connect to IP Address on specified PORT')
        cnct_btn.resize(cnct_btn.sizeHint())
        cnct_btn.clicked.connect(self.connect)
        
        host_edit = QLineEdit()
        port_edit = QLineEdit()

        upld_btn = QPushButton('UPLOAD', self)
        upld_btn.setToolTip('Upload specified file from local folder')
        upld_btn.resize(cnct_btn.sizeHint())
        upld_btn.clicked.connect(self.upload)

        dnld_btn = QPushButton('DOWNLOAD', self)
        dnld_btn.setToolTip('Download specified file from shared folder')
        dnld_btn.resize(dnld_btn.sizeHint())
        dnld_btn.clicked.connect(self.download)

        delt_btn = QPushButton('DELETE', self)
        delt_btn.setToolTip('Download specified file from shared folder')
        delt_btn.resize(delt_btn.sizeHint())
        delt_btn.clicked.connect(self.delete)

        dir_btn = QPushButton('DIR', self)
        dir_btn.setToolTip('List directory contents')
        dir_btn.resize(dir_btn.sizeHint())
        dir_btn.clicked.connect(self.dir)

        grid = QGridLayout()
        grid.addWidget(cnct_btn, 1, 0)
        grid.addWidget(host_edit, 1, 1)
        grid.addWidget(port_edit, 1, 3)

        grid.addWidget(upld_btn, 2, 0)
        grid.addWidget(dnld_btn, 3, 0)
        grid.addWidget(delt_btn, 4, 0)
        grid.addWidget(dir_btn, 5, 0)

        central_wid = QWidget(self)
        self.setCentralWidget(central_wid)
        central_wid.setLayout(grid)
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle("Client Interface")
        self.show()


def main():    
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()