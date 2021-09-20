#!/usr/bin/python3
import socket, sys, time

# create a socket object
# seguimos trabajando con red inet
# DATAGRAMA es el nombre pu de ip
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#get local machine name
host = socket.gethostname()
# host = "" atiende en todas las ip locales
port = int(sys.argv[1])

# bind to the port
serversocket.socket.bind((host, port))

# no tenemos el listen por que no tenemos el seteo del backlog de tcp 
# que servia para acumular las conexiones pendientes hasta que hagan el hanshake
# por que simplemente aca no tenemos hanshake
# las conexiones que entran son datos que voy trabajando directamente

while True:
    # establish a connection
    # me quedo escuchando un dato remoto en vez de escuchar una conexion
    data, addr = serversocket.recvfrom(1024)
    # imprimo la lista de dos elementos
    print(addr)
    # direccion ip
    address = addr[0]
    # puerto
    port = addr[1]
    print("Address: %s - Port %d" % (address, port))
    print("Receiving data: " + data.decode())
    msg =  input("Enter message to send: ").encode()
    serversocket.sendto(msg, addr)
    time.sleep(1)