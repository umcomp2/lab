#!/usr/bin/python3
import socket
import subprocess as sp
import _thread
import pickle

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ""
port = 1234
threadCount = 0
serversocket.bind((host, port))
serversocket.listen(2)

def threaded_client(connection):
    while True:
        data = connection.recv(2048)
        received_command = pickle.loads(data)
        if received_command == 'exit':
            break
        process = sp.Popen([received_command], shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = process.communicate()
        out = pickle.dumps(stdout)
        err = pickle.dumps(stderr)
        if out:
            connection.send(out)
        else:
            connection.send(err)
    connection.close()

while True:
    clientsocket, address = serversocket.accept()
    print("Got a connection from %s" % str(address))
    _thread.start_new_thread(threaded_client, (clientsocket, ))
    threadCount += 1
    print('Thread Number: ' + str(threadCount))