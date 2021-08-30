import socket, argparse
from datetime import datetime


# Obtener por CLI [SERVER] y [PORT]
parser = argparse.ArgumentParser()
parser.add_argument("server", type=str, default='localhost', help="Server IP")
parser.add_argument("port", type=int, default=8000, help="Server PORT")
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
# codeo a bytes el imput del cliente mientras le muestro cual es su ip y puerto antes de entrar al bucle para que sea distinto de exit
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
    print(status_code)
    # repito el mensaje anterior a entrar al bucle
    command = bytes(input(f"cliente_ip:[{SERVER}:{PORT}]$ "), "utf-8")

sock_cli.close()
exit(0)
