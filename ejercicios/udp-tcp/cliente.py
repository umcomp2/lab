#!/usr/bin/python3
import socket as st
import argparse
import sys

parserito_c = argparse.ArgumentParser(description='socket - parte servidor')
parserito_c.add_argument('-i', '--ip', dest = "ip", required = True, help = "ip utilizada")
parserito_c.add_argument('-p', '--port', dest = "puerto", type = int, required = True, help = "Puerto utilizado")
parserito_c.add_argument('-t', '--tipo', dest = "tipo", required = True, help = "protocolo a utilizar")

args = parserito_c.parse_args()

# create a socket object
if args.tipo == "tcp":
    s = st.socket(st.AF_INET, st.SOCK_STREAM)
    host = args.ip
    port = args.puerto
    print("Haciendo el connect")
    s.connect((host, port))   
    print("Handshake realizado con exito!")

    for line in sys.stdin:
        s.send(line.encode("utf-8"))
        
    s.send("exit".encode("utf-8"))
    s.close()
    print("Cerrando la conexion...")

elif args.tipo == "udp":
    s = st.socket(st.AF_INET, st.SOCK_DGRAM)
    host = args.ip
    port = args.puerto
    addr = ((host,port))
    
    for line in sys.stdin:
        s.sendto(line.encode("utf-8"), addr)
    s.sendto("exit".encode("utf-8"), addr)
    s.close()
    print("Cerrando la conexion...")



