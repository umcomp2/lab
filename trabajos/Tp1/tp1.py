from multiprocessing import Process, JoinableQueue
import textwrap
import sys
import argparse
from pathlib import Path
import os


def eliminar_header(image):
    ppm = open(image, encoding='latin1').read()
    header_data = [ppm[:2]]
    in_comment = False
    current_value = ''
    for n, c in enumerate(ppm[2:], 2):
        if len(header_data) == 4:
            header_data.append(n)
            break
        if in_comment:
            if c == '\n':
                in_comment = False
        elif c == '#':
            in_comment = True
        elif c.isspace():
            if current_value:
                header_data.append(int(current_value))
                current_value = ''
        elif c.isdigit():
            current_value += c
    if header_data[0] != 'P6' and header_data[0] != 'P3':
        print('Error, PPM invalido')
        sys.exit()
    sub_char = str(header_data[3])
    indexs = ppm.find(sub_char)
    pixel_data = ppm[indexs:].encode('utf-8')
    pixel_hex = pixel_data.hex()
    exac = pixel_hex[8:]
    img = open('imagen', 'w')
    img.write(exac)
    img.close()


def leer(q1, q2, q3, image, numero):
    eliminar_header(image)
    pr = open('imagen', 'r')
    texto1 = pr.read(numero)
    text = textwrap.wrap(texto1, 2)
    q1.put(text)
    q2.put(text)
    q3.put(text)
    pr.close()


def tomar_rojo(q):
    lista = []
    lista.append(q.get())
    valor = []
    for list1 in lista:
        valor = list1[::3]
    print(valor)
    lista2 = []
    lista2.append('0x')
    lista3 = []
    for v in valor:
        for k in lista2:
            lista3.append(k + v)
    hex_value = []
    for v in lista3:
        an_integer = int(v, 16)
        hex_value.append(an_integer)
    dic = {}
    for i in range(0, 256):
        dic[i] = 0
    for val in hex_value:
        if val not in dic:
            dic[val] = 1
        else:
            dic[val] = dic.get(val) + 1
    lista4 = []
    lista4 = dic.items()
    txt = open('histo_red.txt', 'w')
    for v in lista4:
        txt.write(str(v))
        txt.write('\n')
    txt.close()
    q.close()


def tomar_verde(q):
    lista = []
    lista.append(q.get())
    for list1 in lista:
        valor = list1[1::3]
    print(valor)
    lista2 = []
    lista2.append('0x')
    lista3 = []
    for v in valor:
        for k in lista2:
            lista3.append(k + v)
    hex_value = []
    for v in lista3:
        an_integer = int(v, 16)
        hex_value.append(an_integer)
    dic = {}
    for i in range(0, 256):
        dic[i] = 0
    for val in hex_value:
        if val not in dic:
            dic[val] = 1
        else:
            dic[val] = dic.get(val) + 1
    lista4 = []
    lista4 = dic.items()
    txt = open('histo_green.txt', 'w')
    for v in lista4:
        txt.write(str(v))
        txt.write('\n')
    txt.close()
    q.close()


def tomar_azul(q):
    lista = []
    lista.append(q.get())
    for list1 in lista:
        valor = list1[2::3]
    lista2 = []
    lista2.append('0x')
    lista3 = []
    for v in valor:
        for k in lista2:
            lista3.append(k + v)
    hex_value = []
    for v in lista3:
        an_integer = int(v, 16)
        hex_value.append(an_integer)
    print(hex_value)
    dic = {}
    for i in range(0, 256):
        dic[i] = 0
    for val in hex_value:
        if val not in dic:
            dic[val] = 1
        else:
            dic[val] = dic.get(val) + 1
    lista4 = []
    lista4 = dic.items()
    txt = open('histo_blue.txt', 'w')
    for v in lista4:
        txt.write(str(v))
        txt.write('\n')
    txt.close()
    q.close()


def main():
    parser = argparse.ArgumentParser('Leer imagen PPM')
    parser.add_argument('-s',
                        '--size',
                        help='La cantidad de bytes a leer',
                        required=True,
                        action='store',
                        type=int)
    parser.add_argument('-f',
                        '--file',
                        help='PPM a leer',
                        required=True,
                        action='store',
                        type=str)
    args = parser.parse_args()

    if args.size:
        numero = int(args.size)
        if numero % 6 != 0 or numero < 6:
            print('El numero debe ser multiplo de 6 o mayor a 6')
            sys.exit()
        if args.file:
            tamaño_archivo = Path(args.file).absolute()
            tamaño = os.path.getsize(tamaño_archivo)
            if numero > tamaño:
                print(f'El tamaño a leer debe ser menor al tamaño del archivo.'
                      f'\nNumero introducido: {numero} > Tamaño del archivo: '
                      f'{tamaño}')
                sys.exit()
            imagen = args.file
            if 'ppm' not in imagen:
                print('Error, La imagen debe ser de formato PPM')
                sys.exit()
            q1 = JoinableQueue()
            q2 = JoinableQueue()
            q3 = JoinableQueue()
            leer(q1, q2, q3, imagen, numero)
            p1 = Process(target=tomar_rojo, args=(q1, ))
            p2 = Process(target=tomar_verde, args=(q2, ))
            p3 = Process(target=tomar_azul, args=(q3, ))
            p1.start()
            p2.start()
            p3.start()
            p1.join()
            p2.join()
            p3.join()
            p1.terminate()
            p2.terminate()
            p3.terminate()
            if p1.is_alive() is False and p2.is_alive() is False and \
               p3.is_alive() is False:
                print('Mis hijos han muerto con exito y se han generado sus'
                      ' histogramas')


if __name__ == '__main__':
    main()
