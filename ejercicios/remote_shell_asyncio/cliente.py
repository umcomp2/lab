#!/usr/bin/python3
import socket as st
import argparse
import subprocess as sp

parserito_c = argparse.ArgumentParser(description='socket - parte servidor')
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

comando = bytes(input(), "utf-8")
while comando != b"exit":

    s.send(comando)

    data_recv = str(s.recv(4096), "utf-8")

    print(data_recv)

    comando = bytes(input(), "utf-8") 

    if comando == b"exit":
        s.send(comando)
        break

s.close()
print("Cerrando la conexion...")