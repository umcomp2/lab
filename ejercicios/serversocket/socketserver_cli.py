#!/usr/bin/python3
import socket as st
import argparse
import pickle

parserito_c = argparse.ArgumentParser(description='socket server cliente')
parserito_c.add_argument('-i', '--ip', dest = "ip", required = True, help = "ip utilizada")
parserito_c.add_argument('-p', '--port', dest = "puerto", type = int, required = True, help = "Puerto utilizado")

args = parserito_c.parse_args()

# create a socket object
s = st.socket(st.AF_INET, st.SOCK_STREAM) 
           
host = args.ip
port = args.puerto


print("Haciendo el connect")
s.connect((host, port))   
print("Handshake realizado con exito!")

comando = input()
while comando != "exit":

    serializado = pickle.dumps(comando)

    s.send(serializado)

    data = s.recv(4096)

    data_recv = pickle.loads(data)

    print(data_recv)

    comando = input()

    if comando == "exit":
        serializado2 = pickle.dumps(comando)
        s.send(serializado2)
        break

s.close()
print("Cerrando la conexion...")