import concurrent.futures
import argparse
import os
from typing import List
import ppmparse
import numpy
import threading
import math
import time


def rotate_pixels(color_index: int):
    pixel_index = 0
    block_index = args.n*i
    row, column = [-1, -1]
    original_width = int(ppmParser.metadata[1])
    original_height = int(ppmParser.metadata[2])
    for e in range(len(pixels)):
        pixel_index = block_index + e
        row = int(math.floor(pixel_index/original_width))
        column = pixel_index - original_width*row
        
        new_row = column
        new_column = original_height - 1 - row
        
        ppmMatrix[new_row][new_column][color_index] = pixels[e][color_index]
    return

def submit_workers() -> List:
    red = executor.submit(rotate_pixels, 0)
    green = executor.submit(rotate_pixels, 1)
    blue = executor.submit(rotate_pixels, 2)

    return [red, green, blue]

def write_matrix_to_file():
    fd = os.open("./90.ppm", os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
    new_metadata = "P6\n" + ppmParser.metadata[2] + " " + ppmParser.metadata[1] + "\n255\n"
    os.write(fd, bytes(new_metadata, "UTF-8"))
    
    row_bytes = b""
    for row in ppmMatrix:
        for pixel in row:
            row_bytes += bytes(pixel)
        os.write(fd, row_bytes)
        row_bytes = b""
    
    os.close(fd)

parser = argparse.ArgumentParser()
parser.add_argument("-n", help="Tamaño del bloque de bytes", type=int)
parser.add_argument("-f", help="Archivo a utilizar", type=str)
args = parser.parse_args()

try:
    ppmParser = ppmparse.PPMParser(args.f, args.n)
except FileNotFoundError:
    print("Archivo no encontrado, saliendo...")
    exit(-1)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
ppmMatrix = numpy.ndarray(shape=(int(ppmParser.metadata[1]), int(ppmParser.metadata[2])), dtype=list)

for i in range(ppmMatrix.shape[0]):
    for e in range(ppmMatrix.shape[1]):
        ppmMatrix[i][e] = [0,0,0]

pixels = []
i = 0
while True:
    pixels = ppmParser.getPixels(i*args.n)
    futures = submit_workers()
    for future in futures:
        future.result()
    i += 1
    if len(pixels) != args.n:
        break
print(len(ppmMatrix))
write_matrix_to_file()