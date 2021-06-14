import concurrent.futures
import argparse
import os
from typing import List
import ppmparse
import numpy


def rotate_pixels(color: str):
    colors = {"red": 0, "green": 1, "blue": 2}
    color_index = colors[color[0]]
    pixel_index = 0
    row, column = [-1, -1]
    width = int(ppmParser.metadata[1])
    for e in range(len(pixels)):
        pixel_index = args.n*i + e
        row = int(numpy.floor(pixel_index/width))
        column = pixel_index - width*row
        new_row = column-1
        new_column = ppmMatrix.shape[1] - row-1
        pcolor = pixels[e][color_index]
        ppmMatrix[new_row][new_column][color_index] = pcolor

def submit_workers() -> List:
    red = executor.submit(rotate_pixels, ("red",))
    green = executor.submit(rotate_pixels, ("green",))
    blue = executor.submit(rotate_pixels, ("blue",))

    """red = executor.submit(rot_pixels, (0,))
    green = executor.submit(rot_pixels, (1,))
    blue = executor.submit(rot_pixels, (2,))"""

    return [red, green, blue]


def write_matrix_to_file():
    new_metadata = "P6 " + str(newResolution[0]) + " " + str(newResolution[1]) + " 255\n"
    fd = os.open("./90.ppm", os.O_CREAT | os.O_TRUNC | os.O_RDWR)
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
newResolution = (int(ppmParser.metadata[2]), int(ppmParser.metadata[1]))
ppmMatrix = numpy.ndarray(shape=(newResolution[1], newResolution[0]), dtype=list)

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

write_matrix_to_file()