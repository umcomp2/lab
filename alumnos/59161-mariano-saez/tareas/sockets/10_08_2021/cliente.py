# Escriba un programa cliente/servidor en python que permita ejecutar
# comandos GNU/Linux en una computadora remota.

# Técnicamente, se deberá ejecutar un código servidor en un equipo
# “administrado”, y programar un cliente (administrador) que permita
# conectarse al servidor mediante sockets STREAM.

# El cliente deberá darle al usuario un prompt en el que pueda
# ejecutar comandos de la shell.

# Esos comandos serán enviados al servidor, el servidor los ejecutará,
# y retornará al cliente:

#     la salida estándar resultante de la ejecución del comando
#     la salida de error resultante de la ejecución del comando.

# El cliente mostrará en su consola local el resultado de ejecución
# del comando remoto, ya sea que se haya realizado correctamente o
# no, anteponiendo un OK o un ERROR según corresponda.

# Ejemplo de ejecución del cliente (la salida de los comandos
# corresponden a la ejecución en el equipo remoto.

# diego@cryptos$ python3 ejecutor_cliente.py
# > pwd
# OK
# /home/diego
# > ls -l /home
# OK
# drwxr-xr-x 158 diego diego 20480 May 26 18:57 diego
# drwx------   2 root  root  16384 May 28  2014 lost+found
# drwxr-xr-x   6 andy  andy   4096 Jun  4  2015 user
# > ls /cualquiera
# ERROR
# ls: cannot access '/cualquiera': No such file or directory
# >

# Agregue en el cliente la opción “-l <file>” para permitirle
# al usuario almacenar un log de toda la sesión (comandos
# ejecutados y su fecha/hora).
import socket
import sys
import argparse
from datetime import datetime


# Obtener por CLI [SERVER] y [PORT]
parser = argparse.ArgumentParser()
parser.add_argument("server", type=str, default="127.0.0.1", help="Server IP")
parser.add_argument("port", type=int, help="Server PORT")
parser.add_argument("--file", type=str, default="/dev/null", help="logfile")
args = parser.parse_args()

SERVER = args.server
PORT = args.port
LOGFILE_FD = open(f"{args.file}", "a+")

# Primero creamos un socket del tipo requerido
sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al server
sock_cli.connect((SERVER, PORT))

# Loop para ejectuar comandos remotos
print(f"LOGFILE: {args.file}")
command = bytes(input(f"[vos@{SERVER}:{PORT}]$ "), "utf-8")
while command != b"exit":
    sock_cli.send(command)
    status_code = str(sock_cli.recv(4096), "utf-8")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    LOGFILE_FD.write(f"[{dt_string}] - CMD: {str(command, 'utf-8')} - CODE: {status_code}\n")
    print(status_code)
   
    command = bytes(input(f"[vos@{SERVER}:{PORT}]$ "), "utf-8")

sock_cli.close()
exit(0)
