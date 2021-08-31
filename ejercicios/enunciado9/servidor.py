#!/usr/bin/python3
import socket as st
import time
import argparse
import subprocess as sp

#Argumentos
parserito_s = argparse.ArgumentParser(description='socket - parte servidor')
parserito_s.add_argument('-p', '--port', dest = "puerto", type = int, required = True, help = "Puerto utilizado")

args = parserito_s.parse_args()

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

    while True:

        data = str(socket_cliente.recv(4096), "utf-8")
        datos = data.split()   
        fin = sp.Popen(datos, stdout=sp.PIPE, universal_newlines=True, stderr=sp.PIPE) #, shell=True
        output_full = fin.communicate()
        salida = output_full[0]
        error = output_full[1]
        socket_cliente.send(salida.encode("utf-8"))
        socket_cliente.send(error.encode("utf-8"))

        if not data:
            break

    socket_cliente.close()


    