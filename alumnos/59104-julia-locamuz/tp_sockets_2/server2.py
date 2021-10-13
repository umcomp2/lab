import socket
import os
import time 
import subprocess as sp

# Los sockets stream se basa en el protocolo TCP, que es un protocolo orientado a conexión

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'disconnect'
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

def handle_client(conn, addr): 

    print(f'[NEW CONNECTION] {addr} connected')
    while True:     
        msg = conn.recv(1024).decode(FORMAT)
        if msg == DISCONNECT_MSG: 
            print(f'\n[DISCONNECT] {addr} disconnected')

            break
        else: 
            process = sp.Popen([msg], shell='True', stdout=sp.PIPE, stderr=sp.PIPE)
            stdout, stderr = process.communicate()
            if stdout: 
                msg = b'OK\n'+ stdout
                conn.send(msg)
            else: 
                msg = b'ERROR\n'+ stderr
                conn.send(msg)

    conn.close()


def start():
    print(f'[LISTENING] server is listening on {SERVER}')
    server.listen(5)
    
    while True: 
        # proceso padre acepta conexion
        conn, addr = server.accept()
        # proceso padre crea hijo
        ret = os.fork()
        # proceso hijo se maneja con el cliente dejando al padre disponible para
        # atender otras llamadas
        # if not ret: ((same))
        if ret == 0: # hijo 
            handle_client(conn, addr)
        
print("[STARTING] server is starting...")
start()

