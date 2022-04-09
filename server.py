import socket
import os

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
        self.s.listen(5)
        (clientsocket, address) = self.s.accept()
        with clientsocket:
            print(f"Connected by {address}")
            data = clientsocket.recv(self.BUFFER_SIZE).decode()
            filename, filesize = data.split(self.SEPARATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)
            print(f'{filename}, Size: {filesize}')

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
            
            print(f"Finished uploading {filename}!")


def main():    
    s = Server()
    s.Bind(HOST, PORT)

    while True:
        s.Listen()

if __name__ == "__main__":
    main()