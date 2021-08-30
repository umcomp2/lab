import argparse
import multiprocessing as mp
import socket
import subprocess as sp

# Función argparse para definir puerto
def argumentos():
    parser = argparse.ArgumentParser(description='Shell Server - Comandos')
    parser.add_argument('-p', '--port', type=int, default=1234,
                        help='Puerto de conexión para el server')
    return parser.parse_args()

def comandos(clientsocket, addr):
    while True:
        comando_1 = (clientsocket.recv(256)).decode('utf-8')
        if not comando_1:
            break
        comando_2 = sp.Popen(comando_1.split(), stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        stdout, stderr = comando_2.communicate()
        if stdout:
            resultado = (b'OK\n%s' % stdout)
        elif stderr:
            resultado = (b'ERROR\n%s' % stderr)
        clientsocket.send(resultado)
    print('Conexión con dirección %s y puerto %d finalizada.' % (str(addr[0]), addr[1]))
    clientsocket.close()
    

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Definir host (usar el local)
host = socket.gethostname()
# Definir puerto
args = argumentos()
port = args.port
# Unir puerto con host
serversocket.bind((host, port))
serversocket.listen(3)

print('Esperando conexiones...')
while True:
    # Aceptar y notificar conexión
    clientsocket,addr = serversocket.accept()
    print('Nueva conexión de dirección %s y puerto %d.' % (str(addr[0]), addr[1]))
    mensaje = 'Conexión correcta. Puede proceder.'
    clientsocket.send(mensaje.encode('utf-8'))
    # Crear hijo para ejecutar comandos
    child = mp.Process(target=comandos, args=(clientsocket, addr,))
    child.start()
