#!/usr/bin/python3
import os
import argparse
import signal

def handler (nro, stack):
    global cantidad
    for i in range (cantidad):
        os.wait()
    os.execlp("ps","/usr/bin/ps","-f")
 
print ("Pid: ", os.getpid())

signal.signal(signal.SIGUSR1, handler)
parser = argparse.ArgumentParser(description='ejercicio 1')
parser.add_argument('-n', '--nro',action="store_true", default=False, help="nro")
parser.add_argument('cantidad', type=int, help='cantidad de zombies',metavar='nro')

args =  parser.parse_args()
cantidad = args.cantidad

if (args.nro != True):
    exit(0)

for i in range(cantidad):
    pid = os.fork()
    #hijo
    if pid == 0:
        exit(0)

leido = input("cualquier tecla termina ...")
