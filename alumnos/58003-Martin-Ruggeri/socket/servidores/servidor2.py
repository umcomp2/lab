#!/usr/bin/python3
import socket, sys, time
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
#port = 1234
port = int(sys.argv[1])
# bind to the port
# asociar el socket, (la estructura de memoria) que yo cree con esa tupla
serversocket.bind((host, port))                                  
# queue up to 5 requests
# seteo el barlok de la conexion del socket
# setando la cantidad maxima de conexiones remotas pendientes antes de ser aceptadas
serversocket.listen(2)
# cuando el cliente se conecta y se producia el hansheik 
# syns, syns ask, ask para comenzar a transferir informacion
# estos 3 pasos permite a los dos procesos establecer la conexion
# a partir de ahi tenemos todos los numeros de secuencia y de acnolich
# cuando un cliente hace conect hay un lazo de tiempo entre ese conect hasta que es aceptada
# mientras todavia no se producen los tres mensajes del hanshake la conecion esta inacectada
# entonces es el numero de conecciones pendientes de su hanshake antes que se sean aceptadas
# y al resto le hace drop entonces funciona como un control de negacion de servicio
while True:
    # establish a connection
    print("Esperando conexiones remotas (accept)")
    # accept se queda escuchando en el puerto hasta que llega un cliente y hace un connect 
    clientsocket,addr = serversocket.accept()
    # despues se hace hanshaque
    # asocio al socket del cliente
    # y el puerto de ese cliente remoto
    print("Got a connection from %s" % str(addr))
    
    msg = 'Hola Mundo'+ "\r\n"
    #clientsocket.send(msg.encode('ascii'))
    print("Esperando un tiempito...")
    time.sleep(5)
    print("Enviando mensaje...")
    clientsocket.send(msg.encode('utf-8'))
    print("Cerrando conexion...")
    clientsocket.close()