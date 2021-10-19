import socket
import time


SERVER = "127.0.1.1"
PORT = 2222
ADDR = (SERVER, PORT)
FORMAT = ("utf-8")

#Creo el socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

comandos = ["hello|","email|", "key|","exit"]
time.sleep(1)
for i in comandos:
    if i == "hello|":
        comando = i + input("Ingrese su nombre: ")
    if i == "email|":
        comando = i + input("Ingrese su email: ")
    if i == "key|":
        comando = i + input("Ingrese la única clave válida: ")
    
    if i == "exit":
        comando = input()
    msg = client.send(comando.encode(FORMAT))
    print("Processing")

    dato = client.recv(4096).decode()
    print(dato)

client.close()
print(f"[DISCONNECT] from {ADDR}")