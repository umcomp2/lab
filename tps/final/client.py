
  
import argparse
import socket
import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="ip", type=str)
parser.add_argument("-p", "--puerto", help="puerto", type=int)
parser.add_argument("-r", "--rol", help="Indica que el tipo de usuario", type=str)

argumento = parser.parse_args()

# Crear el socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectar al servidor
    sock.connect((argumento.ip, argumento.puerto))
    if argumento.rol:
        msg_rol = argumento.rol.lower()
        sock.sendall(msg_rol.encode())
    
    if msg_rol == "admin":
        # Si el usuario es un administrador, esperar a que el servidor haga preguntas
        while True:
            pregunta_servidor = sock.recv(1024).decode()
            if pregunta_servidor.startswith("Ingrese "):
                respuesta_usuario = input(pregunta_servidor)
                sock.sendall(respuesta_usuario.encode())
            else:
                break


    # Esperar respuestas del servidor y mostrarlas en la terminal
    while True:
        data = sock.recv(1024)
        print("Respuesta del servidor:", data.decode())

except Exception as e:
    print("Error:", e)
finally:
    sock.close()