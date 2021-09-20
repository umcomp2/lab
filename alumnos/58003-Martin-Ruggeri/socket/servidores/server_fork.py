#!/usr/bin/python3
import socket, sys, time, os

#create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#get local machine name
host = socket.gethostname()
# host = ""
port = int(sys.argv[1])

# bind to the port
serversocket.socket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    #establish a conection
    print("Esperando conexiones remotas (accept)")
    clientsocket, addr = serversocket.accept()
    # cuando viene un cliente y se conecta y hace el hanshake
    # me devuelve una tupla que tiene dos elementos uno es un socket para interactuar con ese cliente
    # y el otro es la direccion del puerto de ese cliente
    # tengo un socket distintos para interactuar con ese cliente puntual

    print("Got a connetion from %s" % str(addr))
    #forkeo
    ret = os.fork()
    # en el caso que sea el hijo empiezo a interactuar con el cliente
    # en el caso que no sea el hijo y sea el padre vuelve a lupear aceptando conexiones
    if not ret: #hijo
        msg = "Hola Mundo" + "\r\n"
        print("Esperando un tiempito...")
        time.sleep(20)
        print("Enviando mensaje...")
        clientsocket.send(msg.encode('utf-8'))
        print("cerrando conexion")
        clientsocket.close()
        exit()

