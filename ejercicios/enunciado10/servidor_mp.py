#!/usr/bin/python3
import socket as st
import multiprocessing as mp
import argparse
import subprocess as sp
import signal

def cliente(socket_c):
    while True:

        data = str(socket_c.recv(4096), "utf-8")
        if data != "exit":
            datos = data.split()
            fin = sp.Popen(datos, stdout=sp.PIPE, universal_newlines=True, stderr=sp.PIPE)
            output_full = fin.communicate()
            salida = output_full[0]
            error = output_full[1]
            socket_c.send(salida.encode("utf-8"))
            socket_c.send(error.encode("utf-8"))
        elif data == "exit":
            break
    socket_c.close()



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
    child = mp.Process(target=cliente, args=(socket_cliente, ))
    child.start()
    


    