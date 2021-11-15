import socket
from argparse import ArgumentParser
import pickle


parser = ArgumentParser()
parser.add_argument('ip_server', help='ip_server')
parser.add_argument('-i',help='ip server', action='store_true')
parser.add_argument('port', help='port')
parser.add_argument('-p',help='port', action='store_true')
parser.add_argument('operacion', help='operacion')
parser.add_argument('-o',help='operacion', action='store_true')
parser.add_argument('primer', help='primer numero')
parser.add_argument('-n',help='primer numero', action='store_true')
parser.add_argument('segun', help='segundo numero')
parser.add_argument('-m',help='segundo numero', action='store_true')
args = parser.parse_args()


parametros = [args.operacion, args.primer, args.segun]


ClientSocket = socket.socket()
host = str(args.ip_server)
port = int(args.port)

print('Waiting for connection')
try:

    print('CONNECTED')
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))


#ClientSocket.send(pickle.dumps(parametros))
#ClientSocket.send(parametros)
ClientSocket.send(pickle.dumps(parametros))
data = pickle.loads(ClientSocket.recv(1024))
print(data)

ClientSocket.close()
