import argparse
import multiprocessing
from pathlib import Path

# Excepciones en caso de algun error


class InvalidHeaderError(Exception):
    pass


class FileEmptyError(Exception):
    pass


class ImageLengthError(Exception):
    pass


def parse_file(file_path, chunk_size):
    img_body = []
    with open(file_path, 'rb') as f:
        # Leemos el header del file.
        first_two_chars = f.readline().splitlines()[0] # Obtenemos el numero magico P6 para verificar si es un ppm.
        if first_two_chars != b'P6':
            raise InvalidHeaderError('Not a ppm file!')
        size_width, size_height = f.readline().split() # Obtenemos el ancho y alto de la imagen.
        max_color = f.readline().splitlines()[0] # Obtenemos el max valor que puede tomar un pixel (1 o 2 byte).
        max_color_val = int(max_color)
        if max_color_val not in (2 ** 8 - 1, 2 ** 16 - 1):
            raise InvalidHeaderError('Maxval is not 1 byte nor 2 bytes!')
        while True:
            # Leemos por bloques el file. ej: 1024
            piece = f.read(chunk_size)
            # Guardamos en la lista la imagen, excluyendo el header.
            comment_started = False
            for p in piece:
                if p == b'\n# ':
                    comment_started = True
                elif comment_started and p == b'\n':
                    comment_started = False
                elif not comment_started:
                    img_body.append(p)
            if not piece:
                break

    expected_len = int(size_width) * int(size_height) * 3 # Verificacion de tamaño esperado con el tamaño de la imagen.
    # 640*426*3 = 817920
    if len(img_body) != expected_len:
        raise ImageLengthError(f'Expected {expected_len} pixels, but got {len(img_body)}')
    # Reconstruyo el header
    nl, space = b'\n', b' ' # newline y espacio.
    header = b''.join((first_two_chars, nl, size_width, space, size_height, nl, max_color, nl))
    return header, img_body, max_color_val


def filter_img(in_queue, scalar, start_offset, max_color_val, name, header):
    if start_offset not in (0, 1, 2):
        raise ValueError('Wrong offset, must be 0, 1 or 2')
    # Para filtrar la imagen dependiendo el offset, si es 0 rojo (scaled_pixel,0,0) / si es 1 verde (0,scaled_pixel,0) / si es 2 (0,0,scaled_pixel)
    img_body = in_queue.get()
    color_filter = []
    for i in range(start_offset, len(img_body), 3):
        if start_offset == 1:  # verde
            color_filter.append(0)
        if start_offset == 2:  # azul
            color_filter.extend([0, 0])
        scaled_pixel = img_body[i] * scalar
        # Verifico que el pixel se encuentre entre [0, 255] or [0, 65535]
        scaled_pixel = min(max(scaled_pixel, 0), max_color_val)
        # Evito numeros decimales para los pixeles . scalar=0.33
        scaled_pixel = int(scaled_pixel)
        color_filter.append(scaled_pixel)
        if start_offset == 0:  # rojo
            color_filter.extend([0, 0])
        if start_offset == 1:  # verde
            color_filter.append(0)
    write_img(name, start_offset, header, color_filter)

# En esta funcion construimos la imagen dependiendo el offset


def write_img(name, offset, header, color_filter):
    channel_type = None
    if offset == 0:
        channel_type = 'r'
    elif offset == 1:
        channel_type = 'g'
    elif offset == 2:
        channel_type = 'b'
    with open(f'{channel_type}_{name}.ppm', 'wb') as out:
        out.write(header)
        out.write(bytes(color_filter))


if __name__ == '__main__':
    # CLI Args
    parser = argparse.ArgumentParser(description='Recuperatorio Tp1 - procesa ppm.')
    parser.add_argument('-r', '--red', type=float, help='Escala para rojo', default=1.0)
    parser.add_argument('-g', '--green', type=float, help='Escala para verde', default=1.0)
    parser.add_argument('-b', '--blue', type=float, help='Escala para azul', default=1.0)
    parser.add_argument('-s', '--size', type=int, help='Bloque de lectura', required=True)
    parser.add_argument('-f', '--file', type=str, help='Archivo a procesar', required=True)
    args = parser.parse_args()

    # Testing
    #args = parser.parse_args(
    #     [
    #         '--red', '2.0',
    #         '--green', '1.0',
    #         '--blue', '1.0',
    #         '--file', 'sample.ppm',
    #         '--size', '1024'
    #     ]
    # )

    # Se crean los procesos hijos y se ejecutan
    file_path = Path(args.file)
    mp_queue = multiprocessing.Queue()

    if not file_path.is_file():
        raise FileNotFoundError('Path does not point to a regular file!')

    if file_path.stat().st_size == 0:
        raise FileEmptyError('File is blank')

    try:
        header, img_body, max_color_val = parse_file(file_path, args.size)

        # (in_queue, scalar, start_offset, max_color_val, name, header)
        name = file_path.stem
        mp_queue.put(img_body)
        mp_queue.put(img_body)
        mp_queue.put(img_body)
        p1 = multiprocessing.Process(target=filter_img, args=(mp_queue, args.red, 0, max_color_val, name, header))
        p2 = multiprocessing.Process(target=filter_img, args=(mp_queue, args.green, 1, max_color_val, name, header))
        p3 = multiprocessing.Process(target=filter_img, args=(mp_queue, args.blue, 2, max_color_val, name, header))
        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()
        print(f'Finished successfully creating 3 files!')

    except (InvalidHeaderError, ImageLengthError, ChildProcessError, ProcessLookupError) as e:
        print(f'Could not dump rgb channels for {file_path}, error: {e}')
