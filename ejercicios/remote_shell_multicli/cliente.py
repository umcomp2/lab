import socket


PORT = 2052
CLIENT = socket.gethostbyname(socket.gethostname())
ADDR = (CLIENT, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = b"\n---DESCONECTADO---"

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsocket.connect(ADDR)

def send(msg):
    mensaje = msg
    clientsocket.send(mensaje)
    print(clientsocket.recv(2048).decode(FORMAT))
    

comando =bytes(input("Elegi un comando: "), FORMAT)
while comando != b"exit" or comando != b"Exit":
    send(comando)
    data = str(clientsocket.recv(1024), FORMAT)
    
    comando = bytes(input("Elegi un comando: "),FORMAT)
    if comando[:4] == b"exit" or comando[:4] == b"Exit":
        send(DISCONNECT_MESSAGE)
        # send(comando)
        break


    # if comando[:4] == 'exit' or comando[:4] == 'Exit':
    #     print("\nADIOS!!")
    #     send(DISCONNECT_MESSAGE)
    #     break
    # else:
    #     send(comando)
    #     comando = bytes(input("Elegi un comando: "),FORMAT)
# clientsocket.close()
# print("\n--CONEXION TERMINADA--")