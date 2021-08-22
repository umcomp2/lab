#!/usr/bin/python3
import socket, sys, time
import subprocess as sp
# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
"""
    socket.AF_INET -> sockets tcp/ip
    socket.AF_UNIX -> sockets Unix (archivos en disco, similar a FIFO/named pipes)
    socket.SOCK_STREAM -> socket tcp, orientado a la conexion (flujo de datos)
    socket.SOCK_DGRAM -> socket udp, datagrama de usuario (no orientado a la conexion)
"""
# get local machine name
host = socket.gethostname()                           
#host = ""
port = 1234 #int(sys.argv[1])
# bind to the port
serversocket.bind((host, port))                                  
# queue up to 5 requests
serversocket.listen(2)
while True:
    # establish a connection
    print("Esperando conexiones remotas (accept)")
    clientsocket,addr = serversocket.accept()      
    print("Got a connection from %s" % str(addr))
    
    client_command = clientsocket.recv(1024)
    #clientsocket.send(msg.encode('ascii'))

    process = sp.Popen([client_command], shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = process.communicate()

    clientsocket.send(stdout)
    clientsocket.send(stderr)

    print("Esperando un tiempito...")
    time.sleep(5)
    #print("Enviando mensaje...")
    #clientsocket.send(msg.encode('utf-8'))
    print("Cerrando conexion...")
    clientsocket.close()