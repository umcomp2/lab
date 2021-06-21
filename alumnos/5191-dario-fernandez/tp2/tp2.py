#!/usr/bin/python3
import concurrent.futures
import sys
import argparse
import os
import mmap

from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Barrier, Lock
from collections import deque

barrier_writer = Barrier(4)
barrier_read = Barrier(4)

index_chunk_row = [0, 0, 0]
index_chunk_col = [0, 0, 0]
thread_color_terminate = [False, False, False]


def get_header_data(ppm_file):
    data_header = {
        'magic_number': None,
        'width': 0,
        'height': 0,
        'max_color': 0,
        'valid': False,
        'position': 0
    }

    magic_number = ppm_file.readline().strip().decode()

    if magic_number in ('P3', 'P6'):
        data_header['magic_number'] = magic_number

    while True:
        line = ppm_file.readline().strip().decode()
        if line.startswith('#'):
            continue
        if len(line.split()) == 2:
            data_header['width'] = int(line.split()[0])
            data_header['height'] = int(line.split()[1])
            continue
        if data_header.get('width') == 0:
            data_header['width'] = line
            continue
        if data_header.get('height') == 0:
            data_header['height'] = line
            continue
        if data_header.get('max_color') == 0:
            data_header['max_color'] = line
            data_header['position'] = 1
            break

    if data_header.get('magic_number') is not None and data_header.get('width') != 0 \
            and data_header.get('height') != 0 and data_header.get('max_color') != 0 \
            and data_header.get('magic_number') != 0:
        data_header['valid'] = True
    return data_header

def rotate_left(block_color_item=None, index_color=None):
    global new_ppm
    global index_chunk_row
    global index_chunk_col
    global color_dimension

    row = color_dimension.get(color).get('rows') - 1 - index_chunk_row[index_color]
    col = index_chunk_col[index_color]

    new_ppm[row][col][index_color] = block_color_item

    if row == 0:
        index_chunk_col[index_color] += 1
        index_chunk_row[index_color] = 0
    else:
        index_chunk_row[index_color] += 1


def rotate_right(block_color_item=None, index_color=None):
    global new_ppm
    global index_chunk_row
    global index_chunk_col
    global color_dimension

    row = index_chunk_row[index_color]
    col = color_dimension.get(color).get('cols') - 1 + index_chunk_col[index_color]

    new_ppm[row][col][index_color] = block_color_item
    if row == color_dimension.get(color).get('rows') - 1:
        index_chunk_row[index_color] = 0
        index_chunk_col[index_color] -= 1
    else:
        index_chunk_row[index_color] += 1

    return None

def process_image(color, sentido):
    global new_ppm
    global block_colors_data
    global thread_color_terminate

    while True:
        # print('BARRIER, ', color)
        barrier_writer.wait()
        block_color = block_colors_data.get(color)
        # index_color = block_colors_data.get(color + '_index')
        index_color = colors.find(color)
        color_block_end = block_colors_data.get(color + '_end')

        for i, x in enumerate(block_color):
            if sentido == 'left':
                rotate_left(block_color_item=x, index_color=index_color)
            else:
                rotate_right(block_color_item=x, index_color=index_color)

        if color_block_end:
            thread_color_terminate[index_color] = True
            break
        barrier_read.wait()

    return color

def create_header_ppm(data=None):
    header = data.get('magic_number') + '\n'
    header += str(data.get('height')) + ' ' + str(data.get('width')) + '\n'
    header += str(data.get('max_color')) + '\n'
    return header


def create_file_output(header=None, direction=None, filename=None):
    global new_ppm

    f_output = direction + '_' + filename
    header_ppm = create_header_ppm(data=header)
    with open(f_output, 'wb') as fo:
        fo.write(bytes(header_ppm.encode()))
        for line in new_ppm:
            a = bytes(list(item for sublist in line for item in sublist))
            fo.write(a)

    fo.close()
    return fo


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TP 1')

    parser.add_argument('-s', '--size', dest="size", required=True, type=int, metavar='bloque de lectura',
                        help='Ingrese cantidad de bytes a leer.')
    parser.add_argument('-f', '--file', action="store", dest="ppm_file", metavar='archivo ppm', type=str,
                        required=True, help="Nombre del archivo PPM")
    parser.add_argument('-sentido', '--sentido', action="store", dest="sentido", metavar='Sentido rotación', type=str,
                        required=False, default='left', choices=['left', 'right'],
                        help="Sentido Rotación PPM")

    options = parser.parse_args()

    header_read = False
    remove_header = True
    init_process = True
    header_data = None

    executor = ThreadPoolExecutor(max_workers=3)
    colors = 'rgb'
    rgb_position = deque('rgb')

    pools = None
    with open(options.ppm_file, 'rb') as f:
        while True:
            if not header_read:
                header_data = get_header_data(f)
                if not header_data.get('valid'):
                    os.write(1, b'Error al leer la cabecera\n')
                    break
                width, height = header_data.get('width'), header_data.get('height')

                color_dimension = {
                    'r': {
                        'rows': header_data.get('width'),
                        'cols': header_data.get('height')
                    },
                    'g': {
                        'rows': header_data.get('width'),
                        'cols': header_data.get('height')
                    },
                    'b': {
                        'rows': header_data.get('width'),
                        'cols': header_data.get('height')
                    }
                }

                new_ppm = [list([None, None, None] for i in range(header_data.get('height'))) for j in
                           range(header_data.get('width'))]
                pools = [executor.submit(process_image, color, options.sentido) for color in colors]
                header_read = True

            ppm_block_data = f.read(options.size)

            block_data = ppm_block_data

            block_colors_data = {}

            for color in colors:
                color_index = next((idx for idx, val in enumerate(rgb_position) if val == color), None)
                block_color = block_data[color_index::3]
                block_colors_data[color] = block_color
                # block_colors_data[color + '_index'] = color_index
                block_colors_data[color + '_end'] = len(ppm_block_data) != options.size

            if len(block_data) % 3 == 1:
                rgb_position.rotate(-1)

            elif len(block_data) % 3 == 2:
                rgb_position.rotate(-2)

            barrier_writer.wait()

            if len(ppm_block_data) != options.size:
                break

            barrier_read.wait()

        # print(barrier_read.parties, barrier_read.broken, barrier_read.n_waiting)
        # print(barrier_writer.parties, barrier_writer.broken, barrier_writer.n_waiting)

    if pools[0].done() and pools[1].done() and pools[2].done():
        print('Terminaron los hilos')
        create_file_output(header=header_data, direction=options.sentido, filename=options.ppm_file)

    f.close()
    sys.exit()
