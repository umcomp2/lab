import argparse
import socket

# Función argparse para definir puerto
def argumentos():
    parser = argparse.ArgumentParser(description='Shell Server - Comandos')
    parser.add_argument('-ht', '--host', type=str, default=socket.gethostname(),
                        help='Host de conexión para el server')
    parser.add_argument('-p', '--port', type=int, default=2222,
                        help='Puerto de conexión para el server')
    return parser.parse_args()

sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Definir host y puerto del servidor
args = argumentos()
host = args.host
port = args.port
# Conectar al host a través del puerto señalado
sockt.connect((host, port))
stage = 0
msg = 'None'
while True:
    if msg == "exit":
        sockt.send(msg.encode('ascii'))
        resultado = sockt.recv(256).decode('ascii')
        if resultado == '200':
            print('Conexión terminada.')
            break
    if stage == 0:
        name = input('Ingrese su nombre: ')
        if name == 'exit':
            msg = 'exit'
            continue
        msg = 'hello|' + name
        sockt.send(msg.encode('ascii'))
        resultado = sockt.recv(256).decode('ascii')
        if resultado == '200':
            print('Ok\n')
            stage = stage + 1
    elif stage == 1:
        email = input('Ingrese su email: ')
        if email == 'exit':
            msg = 'exit'
            continue
        msg = 'email|' + email
        sockt.send(msg.encode('ascii'))
        resultado = sockt.recv(256).decode('ascii')
        if resultado == '200':
            print('Ok\n')
            stage = stage + 1
    elif stage == 2:
        passw = input('Ingrese la contraseña: ')
        if passw == 'exit':
            msg = 'exit'
            continue
        msg = 'key|' + passw
        sockt.send(msg.encode('ascii'))
        resultado = sockt.recv(256).decode('ascii')
        if resultado == '200':
            print('Ok\n')
            stage = stage + 1
        elif resultado == '404':
            print('Clave errónea. Intente nuevamente.\n')
    elif stage == 3:
        end = input('Escriba "exit" para finalizar la conexión: ')
        msg = end
        sockt.send(msg.encode('ascii'))
        resultado = sockt.recv(256).decode('ascii')
        if resultado == '200':
            print('Conexión terminada.')
            break
        elif resultado == '500':
            print('Orden desconocida.\n')
