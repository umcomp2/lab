# Reescribir el ejercicio de remote_shell de modo que permita recibir consultas
# desde varios clientes remotos en forma simultánea. Justifique el uso del
# mecanismo de concurrencia/paralelismo utilizado.
import socket
import sys
import argparse
from datetime import datetime
import pickle


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
cmd_flat = input(f"[vos@{SERVER}:{PORT}]$ ")
while cmd_flat != "exit":
    command = pickle.dumps(cmd_flat)
    sock_cli.send(command)

    serial_exit = sock_cli.recv(4096)
    status_code = pickle.loads(serial_exit)
    

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    LOGFILE_FD.write(f"[{dt_string}] - CMD: {cmd_flat} - CODE: {status_code}\n")
    print(status_code)
   
    cmd_flat = input(f"[vos@{SERVER}:{PORT}]$ ")

sock_cli.send(pickle.dumps("bye"))
sock_cli.close()
exit(0)
