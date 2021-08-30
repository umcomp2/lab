from socket import *

miSocket = socket()

miSocket.connect(('localhost', 8001))

miSocket.send('Hola desde el cliente'.encode())
respuesta = miSocket.recv(1024).decode()

print(respuesta)
miSocket.close()