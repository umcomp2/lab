#!/usr/bin/python3
import socket as st
import argparse
import subprocess as sp

parserito_c = argparse.ArgumentParser(description='socket - parte servidor')
parserito_c.add_argument('-i', '--ip', dest = "ip", required = True, help = "ip utilizada")

args = parserito_c.parse_args()

# create a socket object
s = st.socket(st.AF_INET, st.SOCK_STREAM) 
           
host = args.ip
port = 2222


print("Haciendo el connect")
s.connect((host, port))   
print("Handshake realizado con exito!")

comandos = ["hello|", "email|", "key|", "exit"]

for i in comandos:
    if i == "hello|":
        comando = i + input("Ingrese el nombre: ")
    elif i == "email|":
        comando = i + input("Ingrese el email: ")
    elif i == "key|":
        comando = i + input("Ingrese la key: ")
    if i == "exit":
        comando = input()
    msg = s.send(comando.encode("utf-8"))
    print(".....Datos recibidos.....")
    data = s.recv(4096).decode()
    print(data)
    

s.close()
print("Cerrando la conexion...")