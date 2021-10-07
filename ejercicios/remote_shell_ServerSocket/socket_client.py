import socket
import pickle

PORT = 2064
CLIENT = socket.gethostbyname(socket.gethostname())
ADDR = (CLIENT, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = b"\n---DESCONECTADO---"

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsocket.connect(ADDR)

def send(msg):
    mensaje = msg
    #Serializo el mensaje con el pickle
    serializado = pickle.dumps(mensaje)
    clientsocket.send(serializado)
    print(serializado)
    print(clientsocket.recv(4096))
    

comando =bytes(input("Elegi un comando: "), FORMAT)
while comando != b"exit" or comando != b"Exit":
    send(comando)
    data = str(clientsocket.recv(4096), FORMAT)
    
    comando = bytes(input("Elegi un comando: "),FORMAT)
    if comando == b"exit" or comando == b"Exit":
        send(DISCONNECT_MESSAGE)
        # send(comando)
        break