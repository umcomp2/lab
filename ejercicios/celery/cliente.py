import argparse
import socket
import pickle

#Manejo de argumentos
parser = argparse.ArgumentParser(description = "Calculadora remota con Celery" )

parser.add_argument("-l", "--host", help="host", type=str)
parser.add_argument("-p", "--puerto", dest = "puerto",help="Puerto", type=int)
parser.add_argument("-o", "--operacion", dest= "operacion", help="(suma, resta, mult, div, pot)", type=str)
parser.add_argument("-n", "--n1", dest= "n1", help="numero 1", type=int)
parser.add_argument("-m", "--n2", dest="n2",help="numero 2", type=int)
args = parser.parse_args()

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = args.host
PORT = args.puerto
ADDR = ((HOST, PORT))
socket.connect(ADDR)

msg = [args.operacion, args.n1, args.n2]
serializador = pickle.dumps(msg)
socket.sendall(serializador)
data = socket.recv(1024)
dataDescerializada = pickle.loads(data)
print("El resultado de la operacion es: " + str(dataDescerializada))

print("[SERVER DISCONNECTED]")

socket.close()