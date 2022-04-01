import socket
import sys
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QGridLayout, QWidget, QToolTip, QPushButton, QApplication, QFileDialog)
from PyQt5.QtGui import QFont


#  Test Stuff
#HOST = "127.0.0.1"
#PORT = 65432
#
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def connect(self):
        if self.host_edit.text() == '':
            self.host = "127.0.0.1"
        else:
            self.host = self.host_edit.text()
        
        if self.port_edit.text() == '':
            self.port = 65432
        else:
            self.port = int(self.port_edit.text())

        print(f'Connecting too... {self.host}:{self.port}')

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.host, self.port))
        except ConnectionRefusedError:
            print(f'Connection to {self.host}:{self.port} refused by machine')
            
        self.s.sendall(b"Hello, world")
        data = self.s.recv(1024)
        print(f'RECV\'D FROM SERVER: {data}')


    def upload(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        filenames = []
		
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')
            print(f'Opened {f} for uploading!')
            with f:
                data = f.read()
                self.s.sendall(str.encode(data))
                data = self.s.recv(1024)
                print(f'RECV\'D FROM SERVER: {data}')

    def download(self):
        print("DOWNLOAD")

    def delete(self):
        print("DELETE")
    
    def dir(self):
        print("LIST DIR")

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.cnct_btn = QPushButton('CONNECT', self)
        self.cnct_btn.setToolTip('Connect to IP Address on specified PORT')
        self.cnct_btn.resize(self.cnct_btn.sizeHint())
        self.cnct_btn.clicked.connect(self.connect)
        
        self.host_edit = QLineEdit()
        self.port_edit = QLineEdit()

        self.upld_btn = QPushButton('UPLOAD', self)
        self.upld_btn.setToolTip('Upload specified file from local folder')
        self.upld_btn.resize(self.cnct_btn.sizeHint())
        self.upld_btn.clicked.connect(self.upload)

        self.dnld_btn = QPushButton('DOWNLOAD', self)
        self.dnld_btn.setToolTip('Download specified file from shared folder')
        self.dnld_btn.resize(self.dnld_btn.sizeHint())
        self.dnld_btn.clicked.connect(self.download)

        self.delt_btn = QPushButton('DELETE', self)
        self.delt_btn.setToolTip('Download specified file from shared folder')
        self.delt_btn.resize(self.delt_btn.sizeHint())
        self.delt_btn.clicked.connect(self.delete)

        self.dir_btn = QPushButton('DIR', self)
        self.dir_btn.setToolTip('List directory contents')
        self.dir_btn.resize(self.dir_btn.sizeHint())
        self.dir_btn.clicked.connect(self.dir)

        self.grid = QGridLayout()
        self.grid.addWidget(self.cnct_btn, 1, 0)
        self.grid.addWidget(self.host_edit, 1, 1)
        self.grid.addWidget(self.port_edit, 1, 3)

        self.grid.addWidget(self.upld_btn, 2, 0)

        self.grid.addWidget(self.dnld_btn, 3, 0)
        self.grid.addWidget(self.delt_btn, 4, 0)
        self.grid.addWidget(self.dir_btn, 5, 0)

        self.central_wid = QWidget(self)
        self.setCentralWidget(self.central_wid)
        self.central_wid.setLayout(self.grid)
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle("Client Interface")
        self.show()


def main():    
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()