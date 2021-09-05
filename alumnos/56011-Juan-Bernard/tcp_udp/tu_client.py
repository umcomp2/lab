import argparse
import sys
import socket

# Función argparse para definir host y puerto
def argumentos():
    parser = argparse.ArgumentParser(description='Shell Cliente - Comandos')
    parser.add_argument('-a', '--address', type=str, default=socket.gethostname(),
                        help='Host de conexión para el server')
    parser.add_argument('-p', '--port', type=int, default=2222,
                        help='Puerto de conexión para el server')
    parser.add_argument('-t', '--protocol', type=str, default='tcp',
                        help='Protocolo para la conexión')
    return parser.parse_args()

sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Definir puerto, protocolo y archivo
args = argumentos()
host = args.address
port = args.port
prot = args.protocol

if prot == 'tcp':
    sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockt.connect((host, port))
    mensaje = sockt.recv(256)
    print(mensaje.decode('utf-8'))
    data = sys.stdin.read()
    sockt.send(data.encode('utf-8'))
    resultado = sockt.recv(256)
    print(resultado.decode('utf-8'))
    print('Conexión terminada.')
    sockt.close()
elif prot == 'udp':
    sockt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Escriba lo que quiere enviar.\n')
    data = sys.stdin.read()
    sockt.sendto(data.encode('utf-8'), (host, port))
    resultado = sockt.recvfrom(256)
    print(resultado[0].decode('utf-8'))
    print('Conexión terminada.')
    sockt.close()
else:
    print('\nError.\nProtocolo no reconocido.')
