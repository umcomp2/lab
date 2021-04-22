#!/usr/bin/python3.8

import argparse
import multiprocessing 
import ppmparse
import matplotlib.pyplot as plot

def makeHistogram(color, ipc):
    colors = {"red": 0, "green": 1, "blue": 2}
    color_intensities = []
    while (pixels := ipc.get()) is not None: 
        for pixel in pixels:
            color_intensities.append(pixel[colors[color]])
    else:
        hist = plot.hist(color_intensities, bins=255)
        plot.gcf().savefig("./"+color+".png")
        plot.clf()
    exit()


parser = argparse.ArgumentParser()
parser.add_argument("-n", help="Setea el tamaño del bloque de bytes", type=int)
parser.add_argument("-f", help="Archivo a utilizar", type=str)
args = parser.parse_args()

ipc1 = multiprocessing.Queue()
ipc2 = multiprocessing.Queue()
ipc3 = multiprocessing.Queue()

child1 = multiprocessing.Process(target=makeHistogram, args=("red", ipc1))
child2 = multiprocessing.Process(target=makeHistogram, args=("green", ipc2))
child3 = multiprocessing.Process(target=makeHistogram, args=("blue", ipc3))

child1.start()
child2.start()
child3.start()

ppmParser = ppmparse.PPMParser(args.f, args.n)
# pixels = ppmParser.getPixels(0)
i = 0
while (pixels := ppmParser.getPixels(args.n*i)) != []:
    ipc1.put(pixels)
    ipc2.put(pixels)
    ipc3.put(pixels)

    i += 1

else:
    ipc1.put(None)
    ipc2.put(None)
    ipc3.put(None)


"""for pixel in pixels:
    ipc1.put(pixel)
    ipc2.put(pixel)
    ipc3.put(pixel)
"""


print("## termina padre")
