import socket
import argparse
import sys

parser2 = argparse.ArgumentParser()

parser2.add_argument('port')
parser2.add_argument('-p', action='store_true')
parser2.add_argument('protocol')
parser2.add_argument('-t', help='protocolo transporte', action='store_true')
parser2.add_argument('ip_servidor')
parser2.add_argument('-a', help='ip servidor', action='store_true')

args2 = parser2.parse_args()


if args2.p:
    PORT = int(args2.port) # puerto servidor

if args2.t: 
    PROTOCOL = args2.protocol

if args2.a: 
    IP_SERVER = args2.ip_servidor


ADDR = (IP_SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'disconnect'

if PROTOCOL == 'tcp':
    client = socket.socket()
    client.connect(ADDR)
    for line in sys.stdin: 
        client.send(line.encode())
        if (line).strip() == DISCONNECT_MSG: 
            print('[DISCONNECT]')
            break

elif PROTOCOL == 'udp':
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for line in sys.stdin: 
        client.sendto(line.encode(), ADDR)
        if (line).strip() == DISCONNECT_MSG: 
            print('[DISCONNECT]')
            sys.exit()
            break
    client.sendto(bytes(0), ADDR)