import argparse
import socket
import pickle

#Manejo de argumentos
parser = argparse.ArgumentParser(description = "Calculadora remota con Celery" )

parser.add_argument("-l", "--host", help="Host", type=str)
parser.add_argument("-p", "--port", help="Puerto", type=int)
parser.add_argument("-o", "--operation", help="(suma, resta, mult, div, pot)", type=str)
parser.add_argument("-n", "--number1", help="numero 1", type=int)
parser.add_argument("-m", "--number2", help="numero 2", type=int)
args = parser.parse_args()

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = args.host
PORT = args.port
ADDR = ((HOST, PORT))
socket.connect(ADDR)

msg = [args.operation, args.number1, args.number2]
serializador = pickle.dumps(msg)
socket.sendall(serializador)
data = socket.recv(1024)
dataDescerializada = pickle.loads(data)
print("El resultado de la operacion es: " + str(dataDescerializada))

print("[SERVER DISCONNECTED]")

socket.close()

