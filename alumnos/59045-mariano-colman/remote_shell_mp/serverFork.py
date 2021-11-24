import socket as s
import subprocess, os, sys, time, signal

server = s.socket(s.AF_INET, s.SOCK_STREAM)
server.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

SEPARATOR = "<sep>"
print("[+] SERVIDOR INICIADO")
host = s.gethostbyname(s.gethostname())
port = int(sys.argv[1])

print("\nHost: {} - Puerto: {}".format(host, port))

server.bind((host, port))
server.listen()

signal.signal(signal.SIGCHLD, signal.SIG_IGN)
while True:
    socketCliente, addr = server.accept()
    print("[+]CONEXION ACEPTADA DE {}:{}".format(addr[0], addr[1]))
    directorio = os.getcwd()
    socketCliente.send(directorio.encode())
    cliente = os.fork()
    if not cliente:
        time.sleep(1)
        msj = "Hola cliente n° {}".format(os.getpid())
        socketCliente.send(msj.encode())
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

#s.close()
    #comando = input(f"{msj} $> ")
    #clienteSocket.send(comando.encode())
    #if comando.lower() == "exit":
    #    break