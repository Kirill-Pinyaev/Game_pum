import socket

server_address = 'localhost'
port = 8384

server = socket.socket()
server.bind((server_address, port))
server.listen()
connection, address = server.accept()

while True:
  data = connection.recv(2048)
  if data[0] == 127:
    print("packet recieved")
    connection.send(bytearray([127, 15]))