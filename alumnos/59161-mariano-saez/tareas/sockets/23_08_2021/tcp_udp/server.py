import socket
import argparse as ap


# Obtener los parametros por CLI
parser = ap.ArgumentParser()
parser.add_argument("-p", "--port", type=int,
                    help="Puerto en el que atendera el server",)
parser.add_argument("-t", "--type", type=str,
                    help="Protocolo de capa de transporte TCP/UDP",
                    default="tcp")
parser.add_argument("-f", "--file", type=str,
                    help="Ruta de archivo en el que escribir",
                    default="/dev/null")
args = parser.parse_args()

PORT = args.PORT
TYPE = args.type
FILE = args.file


def tcp():
    # Crear, bindear y poner a escuchar el server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", PORT))
    s.listen()

    # Crear archivo (si no existe antes)
    f = open(f"{FILE}", "w+")

    conn, addr = s.accept()

    while True:
        data = conn.recv(4096).decode()
        






