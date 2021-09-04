import socket
import argparse as ap


def start(proto, port, file):
    # Crear, bindear y poner a escuchar el server
    s = socket.socket(socket.AF_INET, proto)
    s.bind(("0.0.0.0", PORT))
    print(f"Servidor iniciado en puerto {PORT}...")

    # Crear archivo (si no existe antes)
    f = open(f"{FILE}", "w+")

    return s, f


def tcp(s, f):
    s.listen()
    conn, addr = s.accept()
    print(f"Iniciando conexion con {addr}...")

    while True:
        data = conn.recv(4096).decode()
        f.write(data)
        f.flush()
        if data == "":
            print(f"Finalizando conexion con {addr}...")
            conn.close()
            break
        conn.send(b"ACK") # Para habilitar a que envie nuevamente


def udp(s, f):
    while True:
        data, addr = s.recvfrom(4096)
        f.write(data.decode())
        f.flush()

        if data.decode() == "":
            print(f"Finalizando conexion con {addr}...")
            break



if __name__ == "__main__":
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

    PORT = args.port
    FILE = args.file
    if args.type == "tcp":
        TYPE = socket.SOCK_STREAM
    else:
        TYPE = socket.SOCK_DGRAM

    s, f = start(TYPE, PORT, FILE)
    print("\nServidor iniciado con los siguiente parametros:")
    print(f"\tPuerto: {PORT}")
    print(f"\tProtocolo: {args.type.upper()}")
    print(f"\tArchivo destino: {FILE}\n")

    if TYPE == "tcp":
        tcp(s,f)
    else:
        udp(s,f)

    print("Cerrando servidor...")
    f.close()
    s.close()
    exit(0)

    
        






