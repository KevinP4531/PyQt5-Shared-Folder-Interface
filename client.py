import socket
import sys
import os
import time
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
        self.SEPARATOR = "<SEPARATOR>"
        self.BUFFER_SIZE = 4096
    
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


    def upload(self):
        self.s.send(f"UPLOAD".encode())

        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        filenames = []
		
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            print(f'Opened {filenames[0]} for uploading!')
            self.s.send(f"{filenames[0]}{self.SEPARATOR}{os.path.getsize(filenames[0])}".encode())

            with open(filenames[0], "rb") as f:
                tot_sent = 0
                while True:
                    bytes_read = f.read(self.BUFFER_SIZE)
                    tot_sent += len(bytes_read)
                    if not bytes_read:
                        break
                    self.s.sendall(bytes_read)
                    print(tot_sent)
                    
        print("Done Uploading File!")

    def download(self):
        self.s.send(f"DOWNLOAD".encode())
        filename = self.dnld_edit.text()
        self.s.send(filename.encode())

        data = self.s.recv(self.BUFFER_SIZE).decode()
        if (data == "FAILED"):
            print("File does not exist on server!")
        else:
            filename, filesize = data.split(self.SEPARATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)
            print(f'RECEIVING {filename}')

            seconds = (time.time() * 1000) - 500
            first_read = time.time()
            print(seconds)
            down_data = []
            with open(filename, 'wb') as f:
                    sent = 0
                    delta_s = 0.0
                    tot_bytes_read = 0.0
                    while True:
                        bytes_read = self.s.recv(self.BUFFER_SIZE)
                        if not bytes_read:
                            break

                        # Calculate Download Speed
                        delta_s += abs((time.time() * 1000) - seconds)
                        seconds = time.time() * 1000
                        tot_bytes_read += float(len(bytes_read))
                        if delta_s >= 250.0:
                            dnld_speed = tot_bytes_read / delta_s
                            delta_s = 0.0
                            tot_bytes_read = 0.0
                            down_data.append(((seconds/1000) - first_read, dnld_speed)) # Record time since start of transfer, download speed

                        f.write(bytes_read)
                        sent += len(bytes_read)
                        print(f"{float(sent)/filesize}")
            
            with open(f"download_data.txt", 'wb') as f:
                for time_x, speed in down_data:
                    f.write(f"{time_x}, {speed}\n".encode())
            print(f"Finished downloading {filename}!")

    def delete(self):
        self.s.send(f"DELETE".encode())
        filename = self.delt_edit.text()
        if (filename == ''):
            return
        
        print(f'Deleting {filename}...')

        self.s.send(f"{filename}".encode())

        data = self.s.recv(self.BUFFER_SIZE).decode()
        print(f"SERVER MSG: ")

    
    def dir(self):
        self.s.send(f"DIR".encode())
        data = self.s.recv(self.BUFFER_SIZE).decode()
        print(data)

    def exit(self):
        self.s.send(f"EXIT".encode())

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
        self.dnld_edit = QLineEdit()

        self.delt_btn = QPushButton('DELETE', self)
        self.delt_btn.setToolTip('Download specified file from shared folder')
        self.delt_btn.resize(self.delt_btn.sizeHint())
        self.delt_btn.clicked.connect(self.delete)
        self.delt_edit = QLineEdit()

        self.dir_btn = QPushButton('DIR', self)
        self.dir_btn.setToolTip('List directory contents')
        self.dir_btn.resize(self.dir_btn.sizeHint())
        self.dir_btn.clicked.connect(self.dir)

        self.exit_btn = QPushButton('Exit', self)
        self.exit_btn.setToolTip('Terminate Connection')
        self.exit_btn.resize(self.exit_btn.sizeHint())
        self.exit_btn.clicked.connect(self.exit)

        self.grid = QGridLayout()
        self.grid.addWidget(self.cnct_btn, 1, 0)
        self.grid.addWidget(self.host_edit, 1, 1)
        self.grid.addWidget(self.port_edit, 1, 3)

        self.grid.addWidget(self.upld_btn, 2, 0)

        self.grid.addWidget(self.dnld_btn, 3, 0)
        self.grid.addWidget(self.dnld_edit, 3, 1)

        self.grid.addWidget(self.delt_btn, 4, 0)
        self.grid.addWidget(self.delt_edit, 4, 1)

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