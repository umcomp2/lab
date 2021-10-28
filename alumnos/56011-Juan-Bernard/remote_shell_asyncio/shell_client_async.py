import argparse
from datetime import datetime
import os
import socket

# Función argparse para definir host y puerto
def argumentos():
    parser = argparse.ArgumentParser(description='Shell Cliente - Comandos')
    parser.add_argument('-ht', '--host', type=str, default=socket.gethostname(),
                        help='Host de conexión para el server')
    parser.add_argument('-p', '--port', type=int, default=2222,
                        help='Puerto de conexión para el server')
    parser.add_argument('-l', '--log', type=str, default='log.txt',
                        help='Archivo en el que se almacena log')
    return parser.parse_args()

sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Definir host y puerto
args = argumentos()
host = args.host
port = args.port
# Conectar al host a través del puerto señalado
sockt.connect((host, port))
mensaje = sockt.recv(256)
print(mensaje.decode('utf-8'))
log = os.open('%s' % args.log, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
while True:
    # Escribir y enviar comando al server
    comando = input('-> ')
    time = datetime.now()
    time = time.strftime('%d-%m-%Y (%H:%M:%S)')
    data = '-Comando: ' + comando + '\t\t-Fecha: ' + time +'\n'
    os.write(log, data.encode('utf-8'))
    if comando == 'exit':
        sockt.close()
        os.close(log)
        break
    else:
        sockt.send(comando.encode('utf-8'))
        # Recibir y mostrar respuesta
        resultado = sockt.recv(1024) + b'\n'
        os.write(log, resultado)
        print(resultado.decode('utf-8'))
print('Conexión terminada.')
