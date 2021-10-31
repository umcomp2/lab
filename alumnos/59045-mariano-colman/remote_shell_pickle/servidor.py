import socket as s
import threading, pickle, sys, os, time, subprocess, signal

servidor = s.socket(s.AF_INET, s.SOCK_STREAM)
servidor.getsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

HOST = 'localhost'
PORT = int(sys.argv[1])
SEPARATOR = "sep"

servidor.bind((HOST, PORT))

print("[+]SERVIDOR INICIADO!")

servidor.listen()

def consultas(directorio, socketCliente):
    dir = pickle.dumps(directorio)
    socketCliente.send(dir)
    while True:
        comando = socketCliente.recv(1024)
        comando2 = pickle.loads(comando)
        if comando2.lower() == "exit":
            print("\n[+]CONEXION FINALIZADA DE {}:{}".format(addr[0], addr[1]))
            break
        else:
            try:
                output = subprocess.getoutput(comando2)
                rta = f"OK\n{output}"
            except subprocess.CalledProcessError as error:
                rta = f"ERROR\n{output}"
            socketCliente.send(pickle.dumps(rta))
    socketCliente.close()

signal.signal(signal.SIGCHLD, signal.SIG_IGN)
while True:
    socketCliente, addr = servidor.accept()
    print("[+]CONEXION ESTABLECIDA DE {}:{}".format(addr[0], addr[1]))
    directorio = os.getcwd()
    time.sleep(1)
    hilo = threading.Thread(target=consultas, args=(directorio, socketCliente,  ))
    hilo.start()