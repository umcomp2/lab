#!/usr/bin/python3

import socketserver
import pickle
import subprocess as sp

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            data = self.request.recv(1024)
            received_command = pickle.loads(data)
            if received_command == 'exit':
                break
            process = sp.Popen([received_command], shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            stdout, stderr = process.communicate()
            out = pickle.dumps(stdout)
            err = pickle.dumps(stderr)
            if out:
                self.request.send(out)
            else:
                self.request.send(err)
        return

if __name__ == '__main__':
    import socket
    import threading

    address = ('localhost', 0)
    server = socketserver.TCPServer(address, MyTCPHandler)
    ip, port = server.server_address

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)
    t.start()
    # a este punto deberiamos tener un server atendiendo en un puerto particular y esperando conecciones

    # connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    while True:
        command = input("Ingrese el comando a ejecutar: ")
        print("Enviando datos al server")
        msg = pickle.dumps(command)
        s.send(msg)
        if command == "exit":
            break
        print("Reciviendo datos del server")
        new_recv = s.recv(1024)
        recv = pickle.loads(new_recv)
        print(recv.decode())

    server.shutdown()
    s.close()
    server.socket.close()
