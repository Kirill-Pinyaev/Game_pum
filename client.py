import socket

HOST = 'localhost'
PORT = 8008
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(1024)
        print('\nReceived: ', data.decode('utf-8'))
        if 'win' in data.decode('utf-8'):
            break
        if 'strategy' in data.decode('utf-8'):
            mess = input('\nEnter a strategy >>> ')
            mess = mess.encode('utf-8')
            s.sendall(mess)
