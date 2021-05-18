import socket

print('Для выхода из чата наберите: `exit`, `quit` или `q`.')
HOST = '192.168.1.68'
PORT = 8008
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(1024)
        print('\nПолучено: ', data.decode('utf-8'))
        if 'strategy' in data.decode('utf-8'):
            mess = input('\nВведите что нибудь >>> ')
            mess = mess.encode('utf-8')
            s.sendall(mess)
