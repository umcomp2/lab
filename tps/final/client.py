
  
import argparse
import socket
import time
import sys
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="ip", type=str)
parser.add_argument("-p", "--puerto", help="puerto", type=int)
parser.add_argument("-r", "--rol", help="Indica que el tipo de usuario", type=str, default="user")

argumento = parser.parse_args()

#Creo el socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectar al servidor
    sock.connect((argumento.ip, argumento.puerto))
    if argumento.rol:
        msg_rol = argumento.rol.lower()
        sock.sendall(msg_rol.encode())
    
    if msg_rol == "admin":
        respuesta_si_no = int(input("Desea agregar un evento? 1(SI) 2(NO): "))
        if respuesta_si_no == 1:
            while True:
                pregunta_servidor = sock.recv(1024).decode()
                
                if pregunta_servidor.startswith("Ingrese "):
                    respuesta_usuario = input(pregunta_servidor)
                    sock.sendall(respuesta_usuario.encode())    
                else:
                    print("\n" + pregunta_servidor)
                    exit(0)
                    break

    #Espero respuesta del serv. para mostrar por terminal
    while True:
        data = sock.recv(1024)

        if data.startswith(b"INFO"):
            print(data.decode())

        elif data.startswith(b"Gracias por su compra"):
            print(data)
            exit(0)
    
        else:
            print("---Respuesta del servidor----\n", data.decode())
            rta = input("").encode()
            sock.sendall(rta)
           
except Exception as e:
    print("Error:", e)
finally:
    sock.close()

                
    # while True:
    #     data = sock.recv(1024)
    #     if data.startswith(b"RESP:"):
    #         print(data[len(b"RESP:"):].decode())
    #         rta = input("").encode()
    #         sock.sendall(rta)
    #     elif data.startswith(b"INFO:"):
    #         print(data[len(b"INFO:"):].decode())
        
    #     else:
    #         print("----Respuesta del servidor---")
    #         print(data.decode())
        
        


