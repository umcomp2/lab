import socket
import os

mi_socket = socket.socket()
# vamos a hacer la coneccion
# connect recibe una tupla que va a contener dos valores ( la direccion, puerto)
mi_socket.connect(('localhost', 8000))
# vamos a enviar un mensaje
mi_socket.send(bytes("Hola desde el cliente!", encoding = "utf-8"))
# vamos a recibir lo que el servidor nos responda en un bufer de 1024 byte
respuesta = mi_socket.recv(1024)
print(respuesta)
mi_socket.close()
