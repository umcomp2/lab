#!/usr/bin/python3
import os
import argparse
import multiprocessing as mp
import fmanager
import workers

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tp1 - procesa ppm')
    parser.add_argument('-s', '--size',action="store", type= int, required=True, help="Bloque de lectura")
    parser.add_argument('-b', '--bonus',action="store", type= bool, required=False, help="genera archivos con filtros")
    parser.add_argument('-f', '--file',action="store", dest="file", required=True, type=str, help="archivo a procesar")

    args =  parser.parse_args()
    archivo = args.file
    args.size = args.size - (args.size%3) #reajusta a multiplo de 3
    try:
        fd = os.open(archivo, os.O_RDONLY)
    except FileNotFoundError as err:
        print("OS error: {0}".format(err))
        exit(1)
    #manejo de info del encabezado en un modulo
    off,width,height,maxval = fmanager.lee_encabezado(fd)
    os.lseek(fd,off,0) #rebobina al principio del raster
    geometria = [width,height,maxval]
    h = [] #list to save the process
    colors = "rgb"
    for i in colors:
        exec("cola_{} = mp.Queue()".format(i))
        exec('h.append(mp.Process(target=workers.histo, args=(cola_{},i,archivo,geometria,args.bonus)))'.format(i))
        h[-1].start() #el ultimo

    escrito = 0
    while escrito < (width * height * 3): #leyendo de a size ... (si usan mq, el maximo es 32k, si usan pipe , es 8k )
        imorig = os.read(fd, args.size)
        escrito = escrito + len(imorig)
        for i in colors:
            if escrito > (width * height * 3):
                exec('cola_{}.put(imorig[0:(width * height * 3 ) %args.size ])'.format(i)) #por si vienes mas datos que los que corresponden
            else:
                exec('cola_{}.put(imorig)'.format(i))

    for i in range(len(h)):
        h[i].join()
    print ("Se generaron correctamente los" , len(h), "histogramas")
