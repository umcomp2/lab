
  
import argparse
import socket
import pickle

analizador = argparse.ArgumentParser()
analizador.add_argument("-w", "--host", help="Host", type=str)
analizador.add_argument("-p", "--port", help="Puerto", type=int)
analizador.add_argument("-o", "--operation", help="(suma, resta, mult, div, pot)", type=str)
analizador.add_argument("-n", "--number1", help="number 1", type=int)
analizador.add_argument("-m", "--number2", help="number 2", type=int)
argumento = analizador.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST=argumento.host
PORT=argumento.port
serverAddress=((HOST,PORT))
sock.connect(serverAddress)

message = [argumento.operation, argumento.number1, argumento.number2]
pickleMessage = pickle.dumps(message)
sock.sendall(pickleMessage)
data = sock.recv(1024)
pickleReceive=pickle.loads(data)
print('result: '+str(pickleReceive))


print('closing socket')
sock.close()