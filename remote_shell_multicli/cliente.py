import socket

HEADER = 64
PORT = 2030
CLIENT = socket.gethostbyname(socket.gethostname())
ADDR = (CLIENT, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "\n---DESCONECTADO---"

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsocket.connect(ADDR)

def send(msg):
    mensaje = msg.encode(FORMAT)
    print(mensaje)
    tamaño_msg = len(mensaje)
    send_length = str(tamaño_msg).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    clientsocket.send(send_length)
    clientsocket.send(mensaje)
    print(clientsocket.recv(2048).decode(FORMAT))


comando =input("Elegi un comando: ")
while True:
    if comando[:4] == 'exit' or comando[:4] == 'Exit':
        print("\nADIOS!!")
        send(DISCONNECT_MESSAGE)
        break
    else:
        send(comando)
        comando = input("Elegi un comando: ")
# clientsocket.close()
# print("\n--CONEXION TERMINADA--")