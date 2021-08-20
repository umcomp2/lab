import socket
import os

# Los sockets stream se basa en el protocolo TCP, que es un protocolo orientado a conexión

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'disconnect'

server = socket.socket() #el socket.socket() crea por defecto un socket inet y stream

# unimos server con address
# ahora todo lo que se conecte a esa adress will hit this socket 
server.bind(ADDR)

def handle_client(conn, addr): 
    print(f'[NEW CONNECTION] {addr} connected')
    connected = True
    while connected: 
        # vamos a recibir un mensaje de la conexion 'con'
        # FORMAT= bytes --> string 
        msg = conn.recv(1024).decode(FORMAT)
        if msg: 
            if msg == DISCONNECT_MSG: 
                connected = False
                print('[DISCONNECT]')
            else: 
                #print(f'[{addr}] {msg}')   
                if  os.system(msg) == 0:
                    print('OK')
                else: 
                    print('ERROR')

    conn.close()


# funcion que maneja conexiones entrantes
def start():

    print(f'[LISTENING] server is listening on {SERVER}')
    server.listen()
    
    while True: 
        # cuando el server 'capte' una conexion, conn sera el obj socket de esa conexion
        # 
        conn, addr = server.accept()
        handle_client(conn, addr)

print("[STARTING] server is starting...")
start()