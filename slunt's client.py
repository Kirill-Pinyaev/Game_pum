import socket

client = socket.socket()
client.connect(('localhost', 8384))

packet = bytearray([127, 0])

while True:
  choice = int(input())
  if choice == 1:
    client.send(packet)
    data = client.recv(2048)
    if data[0] == 127:
      print("recieve from server", int(data[1]))