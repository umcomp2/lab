import argparse
import multiprocessing as mp
import pickle
import signal
import socket
import subprocess as sp

# Función argparse para definir host y puerto
def argumentos():
    parser = argparse.ArgumentParser(description='Shell Server - Comandos')
    parser.add_argument('-ht', '--host', type=str, default=socket.gethostname(),
                        help='Host de conexión para el server')
    parser.add_argument('-p', '--port', type=int, default=2222,
                        help='Puerto de conexión para el server')
    return parser.parse_args()

def comandos(clientsocket, addr):
    while True:
        comando_0 = clientsocket.recv(256)
        if not comando_0:
            break
        comando_1 = pickle.loads(comando_0)
        comando_2 = sp.Popen(comando_1, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        stdout, stderr = comando_2.communicate()
        if stdout:
            resultado = (b'OK\n%s' % stdout)
        elif stderr:
            resultado = (b'ERROR\n%s' % stderr)
        clientsocket.send(pickle.dumps(resultado))
    print('Conexión con dirección %s y puerto %d finalizada.' % (str(addr[0]), addr[1]))
    clientsocket.close()
    

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Definir host y puerto
args = argumentos()
host = args.host
port = args.port
# Unir puerto con host
serversocket.bind((host, port))
serversocket.listen(3)
# Evitar procesos zombies
signal.signal(signal.SIGCHLD, signal.SIG_IGN)
print('Esperando conexiones...')
while True:
    # Aceptar y notificar conexión
    clientsocket,addr = serversocket.accept()
    print('Nueva conexión de dirección %s y puerto %d.' % (str(addr[0]), addr[1]))
    mensaje = 'Conexión correcta. Puede proceder.'
    clientsocket.send(pickle.dumps(mensaje))
    # Crear hijo para ejecutar comandos
    child = mp.Process(target=comandos, args=(clientsocket, addr,))
    child.start()
