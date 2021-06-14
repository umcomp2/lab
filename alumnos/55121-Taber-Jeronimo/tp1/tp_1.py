"""
Imports
"""
import argparse
import multiprocessing
import re
import os

def child_task(pipe_father,color_child):
    import matplotlib.pyplot as plt

    """
    Funcion principal hijos
    """
    pixels = []
    while True:
        read = pipe_father.recv()
        if read == b'EOF':
            break
        pixels.append(read)
    counted = count_elements(pixels)
    print(dict(sorted(counted.items(), key=lambda item: item[1])))
    save_obj(counted,color_child)
    print(f'Termino el hijo de color: {color_child} y ID:{os.getpid()}')
    plt.hist(pixels, bins=256, color = 'red', edgecolor='blue')
    plt.savefig(f'hist/{color_child}.png')


def count_elements(seq) -> dict:
    """
    Funcion de hijo que cuenta ocurrencias y devuelve un diccionario
    """
    hist = {}
    for i in seq:
        hist[i] = hist.get(i, 0) + 1
    return hist

def save_obj(obj, name ):
    """
    Guarda los diccionarios de colores en un archivo
    """
    with open("dict/"+name + '.txt', 'wt') as file_writer:
        ##ordenadas de menor ocurrencia a mayor
        data = str(dict(sorted(obj.items(), key=lambda item: item[1])))
        file_writer.write(data)




if __name__ == '__main__':

    #Manejador argumentos
    # -f --file
    # -s --size
    parser = argparse.ArgumentParser(description='Histograma RGB imagen - Tp1')
    parser.add_argument('-f',
                        '--file',
                        dest='file',
                        help='archivo a procesar')
    parser.add_argument('-s',
                        '--size',
                        type=int,
                        dest='size',
                        help='Bloque de lectura')
    args = parser.parse_args()
    print (args)

    #Creacion IPC
    pipes = []
    processes = []
    colors = ['Rojo','Verde','Azul']
    for color in colors:
        conn1, conn2 = multiprocessing.Pipe()
        pipes.append(conn1)
        p = multiprocessing.Process(target=child_task, args=(conn2,color))
        p.start()
        processes.append(p)

    #Leer archivo y enviar datos
    with open(args.file, 'rb') as file_reader:
        header = file_reader.readline().strip()
        if header == b'P6':
            print(f"Type: {header}")
        while True:
            header = file_reader.readline().strip()
            if header.startswith(b'#'):
                continue

            match = re.match(br'^(\d+) (\d+)$', header)
            cols, rows = match.groups()
            break

        print (f'Rows: {rows}, cols: {cols}')
        header = file_reader.readline().strip()
        print(f'Max color value: {int(header)}')

        #Leer por bloques y enviar byte correspondiente al hijo
        #pxs = []
        CHILDPICKER=0
        while (block := file_reader.read(args.size).strip()):
            for c in block:
                #print(f'RGB: {c} va a proceso {i}')
                #pxs.append(c)
                pipes[CHILDPICKER].send(c)
                CHILDPICKER += 1
                if CHILDPICKER >= len(colors):
                    CHILDPICKER=0

    #Envia EOF a los hijos y espera a que terminen
    for pipe in pipes:
        pipe.send(b'EOF')
        pipe.close()
    for process in processes:
        process.join()

    print("Termino el padre")
