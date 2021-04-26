#!/usr/bin/python3

import argparse
import os
import sys
import getopt
import time

print("soy el PADRE!!!!" , os.getpid())
pid = os.fork()    # pid hijo


if pid > 0:
    time.sleep(1)
    os.waitpid(pid, 0)
    print("\nsoy el PADRE!!!!" , os.getpid())

else: 

    time.sleep(1)
    print("\nDESDE PROCESO CHILD\n")
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, help='nro posicion 1')
    parser.add_argument('-m', type=int, help='nro posicion 2')
    parser.add_argument('-v', help='verboso', action='store_true')
    args = parser.parse_args()

    print("numero 1: ", args.m)
    print("numero 2: ", args.n)

    promedio = (int(args.n) + int(args.m)) / 2
    if args.v:
        print("Argumentos ingresados:  [('-v', '{}'), ('-n', '{}'), ('-m', '{}')]".format('true', args.n, args.m))

        print("Child's process ID:", pid)

        print("\nI am child process:")
        print("Process ID:", os.getpid())
        print("Parent's process ID:", os.getppid())
        print("promedio {}".format(promedio))
        os.close()

    else:
        print("promedio {}".format(promedio))
        