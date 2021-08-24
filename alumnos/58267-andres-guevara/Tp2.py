import argparse
import os
import threading


def multiplo3(num):
    aprox=int(num-(num%3))
    return aprox

def sheader(fd):
    lectura = os.read(fd, 50)
    lectura = (lectura.split(b'\n'))  
    size = 0
    for i in range(len(lectura)):
        if lectura[i-1] == b'255':   
            break
        size += (len(lectura[i])+1)   
    os.lseek(fd, 0, 0)
    return size

def h_espejado(fd):
    size=sheader(fd)
    header = os.read(fd,size)
    os.lseek(fd,0,0)
    header = str(header, 'utf-8')
    header = header.splitlines()
    h_espejado=str()
    for i in header:
        if '#' not in i:
            if ' ' in i:
                dim = i.split(' ')
                n_ancho = int(dim[0])
                n_alto = int(dim[1])
                dim_espejadas = str(dim[0]+' '+dim[1])
                h_espejado = h_espejado+dim_espejadas+"\n"
            else:
                h_espejado= h_espejado+i+"\n"
    h_espejado = bytes(h_espejado,'utf-8')
    return h_espejado,n_ancho,n_alto



def espejar(ancho,alto,header):
    fotoEntera = open(args.file,'rb')
    body_foto=fotoEntera.readline().splitlines()[0]
    while (body_foto != b"255"):
        body_foto=fotoEntera.readline().splitlines()[0]
    
    pixelestotales= ancho * alto
    pixelesBody = []
    finalEspejado =[]
    final=[]
    for j in fotoEntera.read():
        pixelesBody.append(j)
    
    pixel_individual = []
    fila = []
    for i in pixelesBody:
        pixel_individual.append(i)
        if len(pixel_individual) == 3:
            fila.insert(0,pixel_individual)
            pixel_individual = []
        if len(fila) == ancho:
            finalEspejado.append(fila)
            fila = []
    for i in finalEspejado:
        for j in i:
            for y in j:
                final.append(y) 
    
    red,green,blue=color(final,pixelestotales)
    finalImage = open(f'original_espejado','wb')
    finalImage.write(header)
    finalImage.write(bytes(final))

    return red,green,blue

def color(final,pixelestotales):
    red = []
    green = []
    blue = []
    aux = 0
    while aux != 3*pixelestotales:
        red.append(final[aux])
        aux = aux + 1
        red.append(0)
        red.append(0)  
        green.append(0)
        green.append(final[aux])
        green.append(0)
        aux = aux + 1
        blue.append(0)
        blue.append(0)
        blue.append(final[aux])
        aux = aux + 1

    return red,green,blue

def R_espejado(red,header):
    finalImage = open(f'rojo_espejado','wb')
    finalImage.write(header)
    finalImage.write(bytes(red))

def G_espejado(blue,header):
    finalImage = open(f'blue_espejado','wb')
    finalImage.write(header)
    finalImage.write(bytes(blue))

def B_espejado(green,header):
    finalImage = open(f'green_espejado','wb')
    finalImage.write(header)
    finalImage.write(bytes(green))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TP" - Espeja imagen ppm')
    parser.add_argument('-n', '--valor',action="store", type= int, required=False,default=3, help="Bloque de lectura(Preferentemente un numero multiplo de 3)")
    parser.add_argument('-f', '--file',action="store", required=False, type=str,default='dog.ppm', help="Imagen que se usara")
    args =  parser.parse_args()
    #Chequeo que el archivo exista
    try:
        ppm = os.open(args.file, os.O_RDONLY)
    except FileNotFoundError as err:
        print("No se encontro el archivo")

    header,ancho,alto = h_espejado(ppm)
    red,green,blue = espejar(ancho,alto,header)

t1 = threading.Thread(name="espejado", target=espejar, args=(ancho,alto,header))
t2 = threading.Thread(name="rojo_espejado", target=R_espejado, args=(red,header))
t3 = threading.Thread(name="azul_espejado", target=G_espejado, args=(green,header))
t4 = threading.Thread(name="verde_espejado", target=B_espejado, args=(blue,header))

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

