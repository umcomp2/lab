
  
import argparse
import socket
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="ip", type=str)
parser.add_argument("-p", "--puerto", help="puerto", type=int)
parser.add_argument("-a", "--admin", help="Indica que el usuario es administrador", action="store_true")
parser.add_argument("-c", "--comun", help="Indica que el usuario es común", action="store_true")

argumento = parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(argumento.ip, argumento.puerto)

message = [argumento.operation, argumento.number1, argumento.number2]
pickleMessage = pickle.dumps(message)
sock.sendall(pickleMessage)
data = sock.recv(1024)
pickleReceive=pickle.loads(data)
print('result: '+str(pickleReceive))


print('closing socket')
sock.close()