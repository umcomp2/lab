import socket

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 2222
ADDR =(SERVER, PORT)
FORMAT = 'utf-8'

#creo socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(ADDR)

comandos = ['nombre', 'email', 'key', 'exit']
for i in comandos:
    if i == 'nombre':
        com = input(str("ingrese su nombre: "))
        com = 'hello|' + com
    elif i == 'email':
        com = input(str("ingrese su email: "))
        com = 'email|' + com
    elif i == 'key':
        com = input(str("ingrese una clave: "))
        com = 'key|' + com
    elif i == 'exit':
        com = i
    print("---ENVIANDO DATOS---")
    msg = clientsocket.send(com.encode(FORMAT))
    print("\n---DATOS RECIBIDOS---")
    data = clientsocket.recv(2048).decode()
    print(data)
clientsocket.close()

