#!/usr/bin/python3.8

import argparse
import multiprocessing 
import ppmparse
import matplotlib.pyplot as plot

def makeHistogram(color, ipc):
    values = []
    while (value := ipc.get()) is not None: 
       values.append(value)
    else:
        plot.hist(values, bins=255)
        plot.gcf().savefig("./"+color+".png")
        plot.clf()
    exit()


parser = argparse.ArgumentParser()
parser.add_argument("-n", help="Tamaño del bloque de bytes", type=int)
parser.add_argument("-f", help="Archivo a utilizar", type=str)
args = parser.parse_args()

try:
    ppmParser = ppmparse.PPMParser(args.f, args.n)
except FileNotFoundError:
    print("File not found, exiting...")
    exit(-1)

ipc1 = multiprocessing.Queue()
ipc2 = multiprocessing.Queue()
ipc3 = multiprocessing.Queue()

child1 = multiprocessing.Process(target=makeHistogram, args=("red", ipc1))
child2 = multiprocessing.Process(target=makeHistogram, args=("green", ipc2))
child3 = multiprocessing.Process(target=makeHistogram, args=("blue", ipc3))

child1.start()
child2.start()
child3.start()

i = 0
while True:
    pixels = ppmParser.getPixels(args.n*i)
    for pixel in pixels:
        ipc1.put(pixel[0])
        ipc2.put(pixel[1])
        ipc3.put(pixel[2])
    if pixels[-1] == (None, None, None):
        break
    i += 1

