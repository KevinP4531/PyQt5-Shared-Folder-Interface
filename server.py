import socket

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print(f"Bound: {HOST}:{PORT}")
    s.listen(5)

    while True:
        (clientsocket, address) = s.accept()
        with clientsocket:
            print(f"Connected by {address}")
            data = clientsocket.recv(1024)

            clientsocket.sendall(data)