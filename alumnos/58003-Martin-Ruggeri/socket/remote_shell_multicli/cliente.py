# Reescribir el ejercicio de remote_shell de modo que permita recibir consultas
# desde varios clientes remotos en forma simultánea. Justifique el uso del
# mecanismo de concurrencia/paralelismo utilizado.
import socket
import argparse
from datetime import datetime


# Obtener por CLI [SERVER] y [PORT]
parser = argparse.ArgumentParser()
parser.add_argument("server", type=str, default="127.0.0.1", help="Server IP")
parser.add_argument("port", type=int, help="Server PORT")
parser.add_argument("--file", type=str, default="/dev/null", help="logfile")
# creo mi objeto parser
args = parser.parse_args()

# creo mis constantes 
SERVER = args.server
PORT = args.port
LOGFILE_FD = open(f"{args.file}", "a+")

# Primero creamos un socket del tipo requerido
sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al server
sock_cli.connect((SERVER, PORT))

# Loop para ejectuar comandos remotos
print(f"LOGFILE: {args.file}")
command = bytes(input(f"cliente_ip:[{SERVER}:{PORT}]$ "), "utf-8")
while command != b"exit":
    # itera hasta que el cliente ingrese el comando exit
    # envio el comando al servidor
    sock_cli.send(command)
    #codeo a stream  lo que recivo del servidor
    status_code = str(sock_cli.recv(4096), "utf-8")
    #obtengo la fecha de ejecucion del comando
    now = datetime.now()
    # formateo la fecha
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # imprimo al cliente la respuesta la fecha del servidor
    LOGFILE_FD.write(f"[{dt_string}] - CMD: {str(command, 'utf-8')} - CODE: {status_code}\n")
    # repito el mensaje anterior a entrar al bucle
    print(status_code)
   
    command = bytes(input(f"cliente_ip:[{SERVER}:{PORT}]$ "), "utf-8")

sock_cli.close()
exit(0)
