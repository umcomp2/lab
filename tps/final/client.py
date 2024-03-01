import argparse
import socket
import time
import sys
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="ip", type=str)
parser.add_argument("-p", "--puerto", help="puerto", type=int)
parser.add_argument("-r", "--rol", help="Indica que el tipo de usuario", type=str, default="user")
parser.add_argument("-pr", "--protocolo", help="Ipv6 o Ipv4", type=int)

argumento = parser.parse_args()

#Creo el socket
if argumento.protocolo == 4:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = "10.188.154.219"
else:
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    ip = "::1"

try:
    # Conectar al servidor
    sock.connect((ip, argumento.puerto))
    if argumento.rol:
        msg_rol = argumento.rol.lower()
        sock.sendall(msg_rol.encode())
    
    if msg_rol == "admin":
        respuesta_si_no = int(input("-Si desea agrear un evento presione 1 \n-Si desea eliminar un evento presione 2 "))
        respuesta_si_no_serializada = pickle.dumps(respuesta_si_no)
        sock.sendall(respuesta_si_no_serializada)
        if respuesta_si_no == 1:
            while True:
                pregunta_servidor = sock.recv(1024).decode()
                
                if pregunta_servidor.startswith("Ingrese "):
                    respuesta_usuario = input(pregunta_servidor)
                    sock.sendall(respuesta_usuario.encode())    
                else:
                    print("\n" + pregunta_servidor)
                    exit(0)
        else:
            while True:
                data = sock.recv(1024)
                print("---Respuesta del servidor----\n", data.decode())
                rta = input("").encode()
                sock.sendall(rta)
                
            # while True:
            #     data = sock.recv(1024)
            #     print("---Respuesta del servidor----\n", data.decode())
            #     rta = input("").encode()
            #     sock.sendall(rta)

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

        
        


