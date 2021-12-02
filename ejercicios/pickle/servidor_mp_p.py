#!/usr/bin/python3
import socket as st
import multiprocessing as mp
import argparse
import subprocess as sp
import signal
import pickle

def cliente(socket_c):
    while True:

        data = socket_c.recv(4096)
        data2 = pickle.loads(data)

        if data2 != "exit":
            datos = data2.split()
            fin = sp.Popen(datos, stdout=sp.PIPE, universal_newlines=True, stderr=sp.PIPE)
            output_full = fin.communicate()
            salida = pickle.dumps(output_full[0])
            error = pickle.dumps(output_full[0])
            socket_c.send(salida)
            socket_c.send(error)
        
        elif data2 == "exit":
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

signal.signal(signal.SIGCHLD, signal.SIG_IGN)
while True:
    print("Esperando conexiones remotas (accept)")
    socket_cliente, addr = serversocket.accept()

    print(f"Conexion desde {addr}")
    child = mp.Process(target=cliente, args=(socket_cliente, ))
    child.start()
    


    