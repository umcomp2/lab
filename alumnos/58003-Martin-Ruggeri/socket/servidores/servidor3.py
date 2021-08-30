#!/usr/bin/python3
import socket, subprocess, time, sys, shlex


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname()                           
port = int(sys.argv[1])
serversocket.bind((host, port))                                  
serversocket.listen(2)

print("Esperando conexiones remotas")
while True:
    conn, addr = serversocket.accept()
    print("Got a connection from %s" % str(addr)) 
    data = str(conn.recv(1024), "utf-8")
    command = data.split()
    print(command)
    try:
        returned = subprocess.Popen(command, sys.stdout-subprocess.PIPE, encoding-'utf-8').communicate()[0]
    #conn.send(msg.encode('ascii'))
    print("Esperando un tiempito...")
    time.sleep(5)
    print("Enviando mensaje...")
    conn.send(msg.encode('utf-8'))
    print("Cerrando conexion...")
    conn.close()