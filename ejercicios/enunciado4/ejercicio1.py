#!/usr/bin/python3

import os
import argparse
import signal

def handler (nro, stack):
    global cant
    for i in range (cant):
        os.wait()
    os.execlp("ps","/usr/bin/ps","-f")
 
print ("Pid del proceso padre: ", os.getpid())

signal.signal(signal.SIGUSR1, handler)
parser = argparse.ArgumentParser(description='ejercicio 1')
parser.add_argument('-n', '--nro',action="store_true", default=False, help="nro")
parser.add_argument('cant', type=int, help='cantidad de zombies',metavar='nro')

args =  parser.parse_args()
cant = args.cant

if (args.nro != True):
    exit(0)

for i in range(cant):
    pid = os.fork()
    if pid == 0:   #Proceso hijo
        exit(0)

input("cualquier tecla termina ...")
