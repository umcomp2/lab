#!/usr/bin/python3
import socket as st
import argparse
import subprocess as sp

#Argumentos
parserito_s = argparse.ArgumentParser(description='socket - parte servidor')
parserito_s.add_argument('-p', '--port', dest = "puerto", type = int, required = True, help = "Puerto utilizado")
parserito_s.add_argument('-t', '--tipo', dest = "tipo", required = True, help = "protocolo a utilizar")
parserito_s.add_argument('-f', '--file', dest = "archivo", required = True, help = "archivo a utilizar")

args = parserito_s.parse_args()


if args.tipo == "tcp":
    # create a socket object
    serversocket = st.socket(st.AF_INET, st.SOCK_STREAM) 
    serversocket.setsockopt(st.SOL_SOCKET, st.SO_REUSEADDR, 1)
                          
    host = ""  #por defecto es 0.0.0.0
    port = args.puerto

    serversocket.bind((host, port))                                  
    serversocket.listen(5)

    while True:

        print("Esperando conexiones remotas (accept)")
        socket_cliente, addr = serversocket.accept()
        print(f"Conexion desde {addr}")
        file = open(args.archivo+".txt", "a+")

        while True:

            data = str(socket_cliente.recv(4096), "utf-8")
            file.write(data)

            if data == "exit":
                socket_cliente.close()
                break

elif args.tipo == "udp":
    # create a socket object
    serversocket = st.socket(st.AF_INET, st.SOCK_DGRAM)
    serversocket.setsockopt(st.SOL_SOCKET, st.SO_REUSEADDR, 1)

    host = ""
    port = args.puerto

    # bind to the port
    serversocket.bind((host, port))     

    while True:

        print("Esperando conexiones remotas (accept)")
        data, addr = serversocket.recvfrom(1024)
        print(f"Conexion desde {addr}")
        file = open(args.archivo+".txt", "a+")
        file.write(str(data))
        if data == "exit":
            break

            
        
