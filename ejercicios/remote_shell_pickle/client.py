import socket
import pickle

HEADER = 64
PORT = 5099
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    #Serializo el mensaje con el pickle
    serializado = pickle.dumps(message)
    client.send(serializado)
    print(client.recv(2048).decode(FORMAT))


while True:
    comando = input("Ingrese un comando o exit: ")
    
    if comando[:4] == "exit":
        send(DISCONNECT_MESSAGE)
        break
    else:
        send(comando)