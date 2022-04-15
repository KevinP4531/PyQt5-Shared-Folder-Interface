import socket
import os
from turtle import down

class FileRecord:
    def __init__(self, path, filename, filesize, down_count=0):
        self.name = filename
        self.size = filesize
        self.path = path
        self.down_cnt = down_count
    def __str__(self) -> str:
        return f"{self.name}\t{self.size}\t{self.path}\t{self.down_cnt}"
    def __repr__(self) -> str:
        return f"{self.name},{self.size},{self.path},{self.down_cnt}\n"

class Directory:
    def __init__(self):
        self.entries = {}
    def __str__(self) -> str:
        result = "FILENAME\tFILESIZE\tFILEPATH\tDOWNLOAD COUNT\n"
        for _, entry in self.entries.items():
            result += f"{entry}\n"
        return result
        
    def Add(self, entry):
        if entry.name not in self.entries.keys():
            self.entries[entry.name] = entry


DIR_STRUCT = Directory()
HOST = "127.0.0.1"
PORT = 65432

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SEPARATOR = "<SEPARATOR>"
        self.BUFFER_SIZE = 4096
    
    def Bind(self, host, port):
        self.s.bind((host, port))
        print(f"Bound: {host}:{port}")

    def Listen(self):
        self.s.listen(1)
        (clientsocket, address) = self.s.accept()
        with clientsocket:
            print(f"Connected by {address}")
            data = clientsocket.recv(self.BUFFER_SIZE).decode()

            # process data to get command
            if (data == "UPLOAD"):
                self.ReceiveFile(clientsocket) 
            elif (data == "DOWNLOAD"):
                print("DOWNLOAD")
            elif (data == "DELETE"):
                print("DELETE")
            elif (data == "DIR"):
                self.ListDir(clientsocket)
            else:
                return False
            
            return True
    
    def ListDir(self, cliensocket):
        cliensocket.send(f"{DIR_STRUCT}".encode())

    def ReceiveFile(self, clientsocket):
        data = clientsocket.recv(self.BUFFER_SIZE).decode()
        filename, filesize = data.split(self.SEPARATOR)
        new_entry = FileRecord(filename, os.path.basename(filename), int(filesize))
        filename = os.path.basename(filename)
        filesize = int(filesize)
        print(f'{new_entry}')

        with open(filename, 'wb') as f:
                sent = 0
                while True:
                    bytes_read = clientsocket.recv(self.BUFFER_SIZE)
                    print(bytes_read)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    sent += len(bytes_read)
                    print(f"{float(sent)/filesize}")
        
        DIR_STRUCT.Add(new_entry)
        print(f"Finished uploading {filename}!")


def PopulateFileDirectory():
    with open('./server/directory.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            (filename, filesize, filepath, down_count) = line.split(',')
            DIR_STRUCT.Add(FileRecord(filepath, filename, filesize, down_count))

def WriteFileDirectory():
    with open('./server/directory.txt', 'wb') as f:
        for _,entry in DIR_STRUCT.entries.items():
            f.write(entry.__repr__())

def main():
    PopulateFileDirectory()

    print(DIR_STRUCT)

    s = Server()
    s.Bind(HOST, PORT)

    while s.Listen():
        continue

    WriteFileDirectory()

if __name__ == "__main__":
    main()