#1/usr/bin/python3

import socket, os, threading, sys

def th_server(c):
    print("Launchin proc...")
    # separo la tupla del cliente
    sock, addr = c
    while True:
        msg = sock.recv(1024)
        print("Recibiendo: '%s' de %s" % (msg.decode(), addr))
        msg = "OK" + "\r\n"
        sock.send(msg.encode("utf-8"))

# create a soocket object
# crea un objeto tipo socket para usarlo en la comunicacion
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
port = int(sys.argv[1])

#bind to the port
serversocket.bind((host, port))

#queue up to 5 requests
serversocket.listen(5)

while True:
    # establish a connection
    # cliente es la tupla
    cliente = serversocket.accept()
    clientsocket, addr = cliente
    print("Got a connetion from %s" % str(addr))
    msg = 'Thank you for connecting' + "\r\n"
    clientsocket.send(msg.encode('utf-8'))
    # crea un tread con threading como target el th_server
    # y le paso la tupla completa de cliente
    th = threading.Thread(target=th_server, args=(cliente,))
    # le digo start y vuelve a ciclar y queda colgado de nuevo en el accept
    #mientras el tread esta ejecutando la funcion
    th.start()
