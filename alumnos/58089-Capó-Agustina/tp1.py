import argparse
import multiprocessing as mp
import os
import array
import sys

# definicion de los argumentos
parser = argparse.ArgumentParser(description='tp - procesa ppm')
parser.add_argument('-r', '--red', type=float, default=1,
                    help='Escala para rojo')
parser.add_argument('-g', '--green', type=float, default=1,
                    help='Escala para verde')
parser.add_argument('-b', '--blue', type=float, default=1,
                    help='Escala para azul')
parser.add_argument('-s', '--size', type=int, default=1024,
                    help='Bloque de lectura')
parser.add_argument('-f', '--file', help='Archivo a procesar')
args = parser.parse_args()

try:
    if args.red < 0 or args.green < 0 or args.blue < 0 or args.size <= 0:
        raise ValueError
except ValueError:
    print("Error. Los valores no válidos")
    sys.exit()


def main():
    # abrir archivo
    path = os.path.dirname(os.path.abspath(__file__))
    size = int(args.size)
    try:
        archivo = os.open(path + "/" + args.file, os.O_RDONLY)
    except FileNotFoundError:
        print("No se encontró el archivo")
        sys.exit()
    leido = os.read(archivo, size)

    # sacar comentario
    i = 0
    if i == 0:
        for i in range(leido.count(b"\n# ")):
            barra_n_as = leido.find(b"\n# ")
            barra_n = leido.find(b"\n", barra_n_as + 1)
            leido = leido.replace(leido[barra_n_as:barra_n], b"")

    # sacar encabezado
    primer_n = leido.find(b"\n") + 1
    seg_n = leido.find(b"\n", primer_n) + 1
    ultima_barra_n = leido.find(b"\n", seg_n) + 1
    encabezado = leido[:ultima_barra_n].decode()

    # guardo el cuerpo
    cuerpo = leido[ultima_barra_n:]

    # creo las colas
    queuered = mp.Queue()
    queuegreen = mp.Queue()
    queueblue = mp.Queue()

    # envio primer parte del cuerpo
    queuered.put(cuerpo)
    queuegreen.put(cuerpo)
    queueblue.put(cuerpo)

    # creo hijos
    h_red = mp.Process(target=red, args=(encabezado, queuered))
    h_green = mp.Process(target=green, args=(encabezado, queuegreen))
    h_blue = mp.Process(target=blue, args=(encabezado, queueblue))

    # inicio los hijos
    h_red.start()
    h_green.start()
    h_blue.start()

    # paso el resto del cuerpo
    while True:
        cuerpo = os.read(archivo, args.size)
        queuered.put(cuerpo)
        queuegreen.put(cuerpo)
        queueblue.put(cuerpo)

        if len(cuerpo) != args.size:
            break
    queuered.put("Listo")
    queuegreen.put("Listo")
    queueblue.put("Listo")

    # uno al los hijos con el padre
    h_red.join()
    h_green.join()
    h_blue.join()


    if os.path.exists('red.ppm') and os.path.exists('green.ppm') and os.path.exists('blue.ppm'):
        print("Los archivos han sido creados")
    else:
        print("Los archivos no fueron creados")
 
    # cierro el archivo
    os.close(archivo)


# escalar el color de la imagen
def red(encabezado, queuered):
    imagered = []
    cuerpo = b''
    while True:
        mensaje = queuered.get()
        if mensaje == "Listo":
            break
        else:
            cuerpo = cuerpo + mensaje
    cuerpo_c = [i for i in cuerpo]
    for j in range(0, len(cuerpo_c), 3):
        valor = int(float(cuerpo_c[j]) * float(args.red))
        if valor > 255:
            valor = 255
        imagered.append(valor)
        imagered.append(0)
        imagered.append(0)
    image_red = array.array('B', imagered)
    with open('red.ppm', 'wb') as f:
        f.write(bytearray(encabezado, 'ascii'))
        image_red.tofile(f)


def green(encabezado, queuegreen):
    imagegreen = []
    cuerpo = b''
    while True:
        mensaje = queuegreen.get()
        if mensaje == "Listo":
            break
        else:
            cuerpo = cuerpo + mensaje
    cuerpo_c = [i for i in cuerpo]
    for j in range(1, len(cuerpo_c), 3):
        valor = int(float(cuerpo_c[j]) * float(args.green))
        if valor > 255:
            valor = 255
        imagegreen.append(0)
        imagegreen.append(valor)
        imagegreen.append(0)
    image_green = array.array('B', imagegreen)
    with open('green.ppm', 'wb') as f:
        f.write(bytearray(encabezado, 'ascii'))
        image_green.tofile(f)


def blue(encabezado, queueblue):
    imageblue = []
    cuerpo = b''
    while True:
        mensaje = queueblue.get()
        if mensaje == "Listo":
            break
        else:
            cuerpo = cuerpo + mensaje
    cuerpo_c = [i for i in cuerpo]
    for j in range(2, len(cuerpo_c), 3):
        valor = int(float(cuerpo_c[j]) * float(args.blue))
        if valor > 255:
            valor = 255
        imageblue.append(0)
        imageblue.append(0)
        imageblue.append(valor)
    image_blue = array.array('B', imageblue)
    with open('blue.ppm', 'wb') as f:
        f.write(bytearray(encabezado, 'ascii'))
        image_blue.tofile(f)


if __name__ == "__main__":
    main()
