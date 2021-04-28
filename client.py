import socket


sock = socket.socket()
port = int(input('Введите порт сервера: '))
sock.connect(('localhost', port))
while True:
