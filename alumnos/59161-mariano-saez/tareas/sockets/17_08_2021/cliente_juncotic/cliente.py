import socket
import argparse


# Datos del cliente
datagram = {
    "hello" : None,
    "email" : None,
    "key": None,
}


# Obtener por CLI host y port
parser = argparse.ArgumentParser()
parser.add_argument("-host", type=str, help="Server IP addr")
parser.add_argument("-port", type=int, help="Server port")
args = parser.parse_args()

# Asignarlos
HOST = args.host
PORT = args.port

# Crear socket de la familia INET que trabaje con TCP y establecer conexion
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Conexion exitosa!")

# Solicitar un primer ingreso de datos
for i in datagram:
    datagram[i] = input(f"Ingrese {i}: ")

# Loop que intenta cargar datos hasta que todos los codigos de respuesta
# sean 200
for i in datagram:
    s.send(bytes(f"{i}|{datagram[i]}", "ascii"))
    code = str(s.recv(128), "ascii")
    while code != "200":
        print(f"{i} incorrecto! - CODE: {code} - Intente nuevamente...")
        datagram[i] = input(f"Ingrese {i}: ")
        s.send(bytes(f"{i}|{datagram[i]}", "ascii"))
        code = str(s.recv(128), "ascii")

    print(f"{i} correcto!")

s.send(b"exit")

s.close()