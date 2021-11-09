import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--server_ip',action="store",default='127.0.0.1', type= str)
parser.add_argument('-p', '--port',action="store", type= int, required=True)
parser.add_argument('-o', '--operation',action="store", required=True, type=str)
parser.add_argument('-n', '--n_operand',action="store", required=True, type=str)
parser.add_argument('-m', '--m_operand',action="store", required=True, type=str)
args = parser.parse_args()

ADDR = args.server_ip
PORT = args.port
O = args.operation
N = args.n_operand
M = args.m_operand

msg = bytes(f"{O} {N} {M}","utf-8")
sock = socket.socket()
sock.connect((ADDR, PORT))
sock.send(msg)
resultado = sock.recv(1024)
print(resultado.decode("utf-8"))
