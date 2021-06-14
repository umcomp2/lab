import threading
import argparse
from concurrent.futures import ThreadPoolExecutor
import re

candadoImg = threading.Lock()
barreraLectura = threading.Barrier(4)
barreraEscritura = threading.Barrier(4)
bloque = bytes

def rotador(color, marca, filas, columnas):
    global img_inv
    global bloque
    pos=0
    fila = int(filas) -1
    columna = 0

    print(f"Hijo {color} inicializado")
    barreraLectura.wait()

    while True:

        barreraEscritura.wait()

        if bloque == 'EOF':
            break      

        for c in bloque:
            if pos == marca:

                candadoImg.acquire()
                img_inv[fila][columna][marca] = c
                candadoImg.release()

            pos += 1
            if pos == 3:
                pos = 0
                if fila == 0:
                    fila = filas
                    columna +=1
                fila -= 1
                if columna == columnas:
                    columna = 0

        barreraLectura.wait()

def escribirPPM(file, img):

    file.write(bytearray('P6\n'+
                         str(len(img[0]))+
                         ' '+str(len(img))
                         +'\n255\n'
                         , 'ascii'))
                         
    for row in img:
        for rgb in row:
            file.write(bytes(rgb))

    file.close()

def headerReader(file_reader):
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
    return rows,cols
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Rotacion RGB imagen - Tp2')
    parser.add_argument('-f',
                        '--file',
                        dest='file',
                        help='Archivo a procesar',
                        required=True),
    parser.add_argument('-s',
                        '--size',
                        type=int,
                        dest='size',
                        help='Bloque de lectura',
                        required=True),
    parser.add_argument('-fo',
                        '--fileo',
                        dest='fileo',
                        help='Archivo de salida(Opcional)'),
    
    args = parser.parse_args()
    print (args)

    with open(args.file, 'rb') as file_reader:
        rows, cols = headerReader(file_reader)
        img_inv = [ [[ 0 for i in range(int(3)) ] for j in range(int(rows))]for k in range(int(cols))]

        #Leer por bloques y enviar byte correspondiente a los hilos
        with ThreadPoolExecutor(max_workers=3) as executor:
            future1 = executor.submit(rotador,'Rojo', 0, int(cols), int(rows))
            future2 = executor.submit(rotador,'Verde', 1, int(cols), int(rows))
            future3 = executor.submit(rotador,'Azul', 2, int(cols), int(rows))
            
            while True:
                chunk = file_reader.read(args.size)
                if not chunk or chunk == b'\n': 
                    break
                barreraLectura.wait()
                bloque = chunk
                barreraEscritura.wait()


            barreraLectura.wait()
            bloque = 'EOF'
            barreraEscritura.wait()
  
    if(args.fileo is None):
        file = open("rotado.ppm", "bw")
    else:
        file = open(f"{args.fileo}.ppm", "bw")
    escribirPPM(file,img_inv)

    print("Termino el padre")
