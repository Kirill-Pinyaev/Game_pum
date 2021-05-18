import select
import socket

server_address = '192.168.1.68'
port = 8384
clients = {}

server = socket.socket()
server.bind((server_address, port))
server.listen()

while True:
    connection, address = server.accept()
    data = connection.recv(2048)
    if data[0] == 127:
        print("packet recieved")
        connection.send(bytearray([127, 15]))
