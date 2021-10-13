import argparse
import os.path
import socket


path = "~/cosas.txt"
# Función argparse para definir host y puerto
def argumentos():
    parser = argparse.ArgumentParser(description='Shell Server - Comandos')
    parser.add_argument('-p', '--port', type=int, default=2222,
                        help='Puerto de conexión para el server')
    parser.add_argument('-t', '--protocol', type=str, default='tcp',
                        help='Protocolo para la conexión')
    parser.add_argument('-f', '--file', type=str, default=str(os.path.expanduser(path)),
                        help='Archivo donde se guardará lo escrito')
    return parser.parse_args()

def escribir(file, data):
    # Archivo abierto en modo write, si ya existe, lo sobrescribe
    with open(file, 'w') as text:
        text.write(data)
        resultado = (b'\nOK\n')
        text.close()
    return resultado

# Definir puerto, protocolo y archivo
args = argumentos()
port = args.port
prot = args.protocol
file = args.file
host = '0.0.0.0'

if prot == 'tcp':
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.settimeout(15)
    # Unir puerto con host
    serversocket.bind((host, port))
    serversocket.listen(3)
    print('Esperando conexiones...')
    try:
        while True:
        # Aceptar y notificar conexión
            clientsocket,addr = serversocket.accept()
            print('Nueva conexión de dirección %s y puerto %d.' % (str(addr[0]), addr[1]))
            mensaje = 'Conexión correcta. Escriba lo que quiere enviar.\n'
            clientsocket.send(mensaje.encode('utf-8'))
            data = (clientsocket.recv(1024)).decode('utf-8')
            resultado = escribir(file, data)
            clientsocket.send(resultado)
            clientsocket.close()
    except socket.timeout:
        print('Finalizando conexión del servidor.')
elif prot == 'udp':
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((host, port))
    serversocket.settimeout(30)
    print('Esperando conexiones...')
    try:
        while True:
            data, addr = serversocket.recvfrom(1024)
            print('Nueva conexión de dirección %s y puerto %d.' % (str(addr[0]), addr[1]))
            resultado = escribir(file, data.decode('utf-8'))
            serversocket.sendto(resultado, addr)
    except socket.timeout:
        print('Finalizando conexión del servidor.')
else:
    print('\nError.\nProtocolo no reconocido.')
