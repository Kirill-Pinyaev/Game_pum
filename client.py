import socket
import sys
import select


server = socket.socket()
server.bind(('localhost', 6666))
server.listen(5)
slov = {}
while True:
    clients = slov.keys()
    conn, addr = server.accept()
    sockets = [sys.stdin, server] + clients
    print(sockets)
    ins, _, _ = select.select(sockets, [], [], 0)
    for i in ins:
        if i is server:
            slov[conn] = addr
        else:
            data = conn.recv(4)
            if not data:
                conn.close()
                conn.send(b'hell')
