
  
import argparse
import socket
import time
import sys

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
                    break
    # else:
    #     # Aquí se maneja la interacción para el caso de usuario, si es necesario enviar una respuesta al servidor
    #     # Por ejemplo, si el servidor pregunta por el número del evento, aquí podrías enviar la respuesta.
    #     respuesta_evento = input("Ingrese el número del evento que desea ver: ")
    #     sock.sendall(respuesta_evento.encode())
        

    #Espero respuesta del serv. para mostrar por terminal
    while True:
        data = sock.recv(1024)
        print("---Respuesta del servidor----\n", data.decode())
        rta = input("").encode()
        sock.sendall(rta)
        


except Exception as e:
    print("Error:", e)
finally:
    sock.close()