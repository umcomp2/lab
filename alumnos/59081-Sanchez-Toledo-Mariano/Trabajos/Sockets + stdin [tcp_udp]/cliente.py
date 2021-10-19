import argparse
from parseCliente import Parse
from socket import *
from sys import stdin
import pickle

def runTCP(socket):
    print(pickle.loads(socket.recv(1024)))
    data = stdin.read()
    socket.send(pickle.dumps(data))

def runUDP(socket):
    print('Ingrese texto:')
    data = stdin.read()
    socket.send(pickle.dumps(data))

def main():
    args = Parse.parser()
    if args.type == 'udp':
        miSocket = socket(AF_INET, SOCK_DGRAM)
        miSocket.connect((args.a, args.port))
        runUDP(miSocket)

    elif args.type == 'tcp':
        miSocket = socket(AF_INET, SOCK_STREAM)
        miSocket.connect((args.a, args.port))
        runTCP(miSocket)
    
    exit(0)

if __name__ == '__main__':
    main()
