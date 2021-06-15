#!/usr/bin/python3
import os
import argparse
import sys
from multiprocessing import Process, Pipe
import re


# devuelve una lista de largo 256 y sus items van del o al 255
def profundidad():
    prof = list()
    count = 0
    for i in range(256):
        prof.append(count)
        count += 1
    return prof


# devuelve la frecuencia absoluta de cada pixel
def histo(color_list):
    profundidad = list()
    total = list()
    count = 0

    for i in range(256):
        profundidad.append(count)
        count += 1
    
    for i in profundidad:
        qt = 0
        for j in color_list:
            if i == j:
                qt += 1
        total.append(qt)
    return (total)


# hace que lea el array de a 3 posiciones. K indica el punto de partida.
def rgb_list(arr_rgb, k):
    lista = arr_rgb[k::3]
    return lista
    

def histogram(hijo, color, name):
    rgb = list()
    
    
    while True:

         # Histograma para color r
        if color == 'r':
            
            # recibe todo lo que hay en el pipe
            texto = hijo.recv()

            # agrega cada byte a la lista con todos los pixeles
            for byte in texto:
                rgb.append(byte)

            # crea una nueva lista en la que solo lee los pixeles rojos. Por eso empieza a contar desde la posicion 0.
            r = rgb_list(rgb, 0)

            # busca el EOF.
            if texto == b"":

                 # Intenta crear un arhivo del tipo color_file.txt. Si este ya existe levanta un error y devuelve un exitcode = 1.
                try:
                    txt = os.open('{}_{}{}'.format(color, name, 'txt'), os.O_RDWR  | os.O_CREAT | os.O_EXCL)
                except FileExistsError:
                    sys.stdout.write('ERROR. File "{}_{}{}" already exists\n'.format(color, name, 'txt'))
                    sys.exit(1)

                # si pudo crear el archivo exitosamente, arma el histograma y lo escribe en el archivo creado               
                hist = histo(r)
                prof = 0
                for i in range(len(hist)):
                    line = (str(hist[i]))
                    os.write(txt, (('{}: {}\n').format(prof, line)).encode())
                    prof += 1
                os.close(txt)
                  
                break
            
                
########################################################################################################

        # Histograma para color g
        if color == 'g':

            # recibe todo lo que hay en el pipe
            texto = hijo.recv()

            # agrega cada byte a la lista con todos los pixeles
            for byte in texto:
                rgb.append(byte)

            # crea una nueva lista en la que solo lee los pixeles verdes. Por eso empieza a contar desde la posicion 1.
            g = rgb_list(rgb, 1)

            # busca el EOF.
            if texto == b"":

                # Intenta crear un arhivo del tipo color_file.txt. Si este ya existe levanta un error y devuelve un exitcode = 1.
                try:
                    # txt = os.open('{}_{}{}'.format(color, name, 'txt'), os.O_RDWR  | os.O_CREAT | os.O_TRUNC)
                    txt = os.open('{}_{}{}'.format(color, name, 'txt'), os.O_RDWR  | os.O_CREAT | os.O_EXCL)
                except FileExistsError:
                    sys.stdout.write('ERROR. File "{}_{}{}" already exists\n'.format(color, name, 'txt'))
                    sys.exit(1)

                # si pudo crear el archivo exitosamente, arma el histograma y lo escribe en el archivo creado
                hist = histo(g)
                prof = 0
                for i in range(len(hist)):
                    line = (str(hist[i]))
                    os.write(txt, (('{}: {}\n').format(prof, line)).encode())
                    prof += 1
                os.close(txt)
                    
                break

            
##########################################################################################

        # Histograma para color b
        if color == 'b':

            # recibe todo lo que hay en el pipe
            texto = hijo.recv()

            # agrega cada byte a la lista con todos los pixeles
            for byte in texto:
                rgb.append(byte)
            
            # crea una nueva lista en la que solo lee los pixeles azules. Por eso empieza a contar desde la posicion 2.
            b = rgb_list(rgb, 2)

            # busca el EOF. 
            if texto == b"":
                
                # Intenta crear un arhivo del tipo color_file.txt. Si este ya existe levanta un error y devuelve un exitcode = 1.
                try:
                    txt = os.open('{}_{}{}'.format(color, name, 'txt'), os.O_RDWR  | os.O_CREAT | os.O_EXCL)
                except FileExistsError:
                    sys.stdout.write('ERROR. File "{}_{}{}" already exists\n'.format(color, name, 'txt'))
                    sys.exit(1)

                # si pudo crear el archivo exitosamente, arma el histograma y lo escribe en el archivo creado
                hist = histo(b)
                prof = 0
                for i in range(len(hist)):
                    line = (str(hist[i]))
                    os.write(txt, (('{}: {}\n').format(prof, line)).encode())
                    prof += 1
                os.close(txt)
                break
            
            

    # cierra el los 3 pipes.
    hijo.close()     
    return 
    
        
# determina el largo del header através de regex
def header(f):
    while True:
        # lee un maximo de 256 bytes 
        fd = os.read(f, 256)
        # decodea los bytes para que puedan ser entendidos por las regex.
        text = fd.decode('utf-8', 'replace')
        head_lenght = 0
        # busca si es P6 o P3
        regex = re.compile(r"(P6|P3)")
        # busca comentarios
        regex_comment = re.compile(r"\n(#\s*.*){1}")
        # busca largo * ancho
        regex3 = re.compile(r'\n(600|5[0-9][0-9]|4[0-9][0-9]|3[0-9][0-9]|2[0-9][0-9]|1[0-9][0-9]|[1-9]?[0-9]){1}\s(500|4[0-9][0-9]|3[0-9][0-9]|2[0-9][0-9]|1[0-9][0-9]|[1-9]?[0-9]){1}')
        # busca profundidad
        regex4 = re.compile(r'\n(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\n')
        h1 = regex.search(text)
        h2 = regex_comment.search(text)
        h3 = regex3.search(text)
        h4 = regex4.search(text)
        list_regex = [h1, h2, h3, h4]
        for i in list_regex:
            if i:
                # cada vez que la regex hace un match, sume el largo de esa cadena al largo del header
                head_lenght += len(i.group().encode())
        
        # devuelve el largo del encabezado
        return int(head_lenght)
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='TP1 - procesa ppm')
    parser.add_argument('-s', '--size',action="store", metavar='SIZE', type=int,
                        required=True, help='Bloque de lectura')
    parser.add_argument('-f', '--file',action="store", metavar='FILE', type=str,
                        required=True, help='archivo a procesar')

    args = parser.parse_args()
    fd = args.file
    chunk = args.size

    # lista de parent connections
    parent_conn = list()
    # lista de child connections
    hijos = list()
    # lista rgb 
    colors = ['r', 'g', 'b']
    index = 0
    #regex para que traiga el nombre. Ejemplo: tux.
    regex = re.compile(r'.*\.')
    name = regex.match(fd).group()

    # crea los 3 procesos hijos y targetea a la funcion histogram
    # Le paso los argumentos: h (pipe), colors(r,g o b) y el nombre
    for i in range(3):
        p, h = Pipe()
        
        child = Process(target=histogram, args=(h, colors[index], name))
        index += 1
        #agregamos los hijos a la lista
        hijos.append(child)
        
        parent_conn.append(p)

    # inicializamos a los hijos
    for i in hijos:
        i.start()
    
    # Manejo de error File not found
    try:
        fd_read = os.open(fd, os.O_RDWR)

        head_lenght = header(fd_read)
        # empieza a leer desde el final del header
        os.lseek(fd_read, head_lenght, 0)
    except FileNotFoundError:
        sys.stdout.write('ERROR. Fiñe "{}" does not exist.\n'.format(fd))
        for i in hijos:
            # Si hubo un error, mata a los hijos y termina
            i.kill()    
        sys.exit(1)
    
    # Lee el archivo ppm de a chunks y temina con el EOF
    while True:
        f_read = os.read(fd_read, chunk)
        parent_conn[0].send(f_read)
        parent_conn[1].send(f_read)
        parent_conn[2].send(f_read)
    
        if f_read == b"" and len(f_read) < chunk:
            break
    os.close(fd_read)

    #esperan a que terminen
    for i in hijos:
        i.join()
        

    for i in parent_conn:
        i.close()
    
    errores = 0
    # si se encuentra con uun error, el hijo envia un exitcode = 1
    # cuenta los errores e imprime el error
    for i in hijos:
        if i.exitcode == 1:
            errores +=1
    # si no hubieron errores, envia por stdout un mensaje de exito.
    if errores == 0:
        sys.stdout.write('Se generaron correctamente los 3 histogramas \n')
        
