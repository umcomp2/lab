import argparse
from os import path, truncate
import re
import threading
import time
from typing import final

# Defino el parse

parser = argparse.ArgumentParser(description="Image processing")

parser.add_argument('-f','--fileImage',
required=False,
default='dog.ppm',
type=str,
help='File of the image')

parser.add_argument('-s','--size',
default=255,
type=int,
help='Size of the image')

parser.add_argument('-r','--red',
default=1,
type=float,
help='intensity of red')

parser.add_argument('-g','--green',
default=1,
type=float,
help='intensity of green')

parser.add_argument('-b','--blue',
default=1,
type=float,
help='intensity of blue')

parser.add_argument('-c','--colour',
default=1,
type=float,
help='intensity of color')

parser.add_argument('-rot','--rotation',
default=False,
type=bool,
help='True if you want to rotate')

parser.add_argument('-mir','--mirror',
default=False,
type=bool,
help='True if you want to mirror')

# Fx para extraer los valores imporantes del header

def Header(file):
    aux = 0
    flag1 = False
    flag2 = False
    while(aux != 10):


        # Leo de a lineas y spliteo 

        line = file.readline().splitlines()[0]
        coment = re.search(b'#',line)

        # Es comentario?

        if(coment != None):
            aux = aux + 1
            continue

        # Es el magic number?

        if(line == b'P6'):
            flag1 = True
            form = line
            aux = aux +1
            continue

        # Son las dimenciones?

        if(flag1):
            flag2 = True
            width,height = line.split()
            flag1 = False
            aux = aux +1
            continue

        # Es el max color?

        if(flag2):
            maxCol = line
            aux = aux +1
            break
    return form, width, height, maxCol             
        
# Fx para generar la lista de valores de los pixeles correspondientes al rojo, verde, azul como el full color 
        
def Body(file,size):

    # Variables auxiliares

    listRed = []
    listGreen = []
    listBlue = []
    listAll = []
    pixelCant = int(width)*int(height)
    f1,f2,f3 = True,False,False
    
    # Mientras cada lista no tenga la cantidad de pixeles que debe tener al final se seguiran completando 

    while(len(listRed) != pixelCant or len(listGreen) != pixelCant or len(listBlue) != pixelCant):
        byteRead = file.read(size)
        for f in byteRead:

            # Lee valor para rojo y habilita la proxima lectura del verde

            if(f1):
                if(len(listRed) == pixelCant):
                    continue
                listRed.append(f)
                listAll.append(f)
                f1 = False
                f2 = True
                continue

            # Lee valor para verde y habilita la proxima lectura del azul

            if(f2):
                listGreen.append(f)
                listAll.append(f)
                f2 = False
                f3 = True
                continue


            # Lee valor para azul y habilita la proxima lectura del rojo

            if(f3):
                listBlue.append(f)
                listAll.append(f)
                f3 = False
                f1 = True
                continue    


    return listRed,listGreen,listBlue,listAll

# Fx para armar la imagen 

def ImageProcessing(name,body,colour,multiplier,maxCol,headerR,headerNotR,rotationBool,mirrorBool,w,h):
    
    # Variables auxiliares
    
    newImageBody = []
    newImageBodyColour = []

    # Voy leyendo el body

    for i in body:

        # Si la hay, aplico la intensidad del color

        finalPixel = multiplier*i
        finalPixel = int(min(max(finalPixel,0),int(maxCol)))
        
        # Relleno los pixeles exluyentes con valores nulos, ya sea para el caso de rojo, verde o azul y siempre para el full color


        newImageBodyColour.append(finalPixel)

        if colour == "green":
            newImageBody.append(0)
        if colour == "blue":
            newImageBody.append(0)
            newImageBody.append(0)
        newImageBody.append(finalPixel)
        if colour == "red":
            newImageBody.append(0)
            newImageBody.append(0)
        if colour == "green":
            newImageBody.append(0)
    

    # Se le da a la funcion que constuye la nueva imagen los parametros necesarios para que esta opere

    if colour == "red":

        if rotationBool:
            aux = w
            w = h
            h = aux
            newImageBody = RotateBody(newImageBody,w,h)
            NewImageMaker(name,"red",newImageBody,headerR,1)
        
        if(mirrorBool):
            newImageBody = MirrorBody(newImageBody,w,h)
            NewImageMaker(name,"red",newImageBody,headerNotR,2)
        
    if colour == "green":

        if rotationBool:
            aux = w
            w = h
            h = aux
            newImageBody = RotateBody(newImageBody,w,h)
            NewImageMaker(name,"green",newImageBody,headerR,1)
        
        if(mirrorBool):
            newImageBody = MirrorBody(newImageBody,w,h)
            NewImageMaker(name,"green",newImageBody,headerNotR,2)

    if colour == "blue":

        if rotationBool:
            aux = w
            w = h
            h = aux
            newImageBody = RotateBody(newImageBody,w,h)
            NewImageMaker(name,"blue",newImageBody,headerR,1)
        
        if(mirrorBool):
            newImageBody = MirrorBody(newImageBody,w,h)
            NewImageMaker(name,"blue",newImageBody,headerNotR,2) 

    if colour == "colour":

        if rotationBool:
            aux = w
            w = h
            h = aux
            newImageBody = RotateBody(newImageBodyColour,w,h)
            NewImageMaker(name,"color",newImageBody,headerR,1)
        
        if(mirrorBool):
            newImageBody = MirrorBody(newImageBodyColour,w,h)
            NewImageMaker(name,"color",newImageBody,headerNotR,2)    
       

# Termina de armar la imagen con todos los nuevos parametros, header, body y genera el archivo.pmm de salida

def NewImageMaker(name,colour,newImageBody,header,case):

    # Para el caso de rotado

    if(case == 1):
        finalImage = open(f'{colour}_rotated_{name}','wb')
        finalImage.write(header)
        finalImage.write(bytes(newImageBody))
    
    # Para el caso de mirror

    if(case == 2):
        finalImage = open(f'{colour}_mirror_{name}','wb')
        finalImage.write(header)
        finalImage.write(bytes(newImageBody))

    # Para el caso de no rotado ni mirror

    if(case == 3):
        finalImage = open(f'{colour}_{name}','wb')
        finalImage.write(header)
        finalImage.write(bytes(newImageBody))

#reconstruyo el nuevo header

def RemakingHeader(form,width,height,maxCol,rotationBool,mirrorBool):
    if rotationBool:
        newHeader = b''.join((form,b'\n',height,b' ',width,b'\n',maxCol,b'\n'))
    if mirrorBool:
        newHeader = b''.join((form,b'\n',width,b' ',height,b'\n',maxCol,b'\n'))
    return newHeader

#en el caso de rotar la imagen se rota en esta funcion

def RotateBody(body,w,h):

    # Variables auxiliares

    newBody = []
    row = []
    pixel = []
    newBodyRotated = []
    finalList = []
    originalRowCuantity = int(w)
    originalColCuantity = int(h)
    pixelsShouldHave = int(originalColCuantity)*int(originalRowCuantity)*3
    
    # Genero una matriz de la imagen

    for i in body:
        pixel.append(i)
        if len(pixel) == 3:
            row.append(pixel)
            pixel = []
        if len(row) == int(h):
            newBody.append(row)
            row = []
        
    # Busco nuevas dimensiones y chequeo que correspondan a las correspondientes de la imagen original (no rotada)

    rotatedColCuantity = len(newBody)
    rotatedRowCuantity = len(newBody[1])

    if rotatedColCuantity == originalRowCuantity and rotatedRowCuantity == originalColCuantity:
        print("Match confirm: new and old dimensions parameters")
    
    # Roto la matriz (roto la imagen)
    
    newBodyRotated = list(zip(*newBody[::-1]))        
       
    # Vuelco el contenido de la matriz en una lista y confirmo que ambas imagenes tengan la misma cantidad de pixeles

    for i in newBodyRotated:
        for j in i:
            for y in j:
                finalList.append(y)

    if len(finalList) == pixelsShouldHave:
        print('Match confirm: new and old pixels cuantity')
    
    # Retorno la nueva lista rotada

    return finalList

# Fx para reflejar la imagen

def MirrorBody(body,w,h):
    
    # Varriables auxiliares
    
    newBody = []
    row = []
    pixel = []
    finalList = []
    
    # Genero matriz del boddy
    
    for i in body:
        pixel.append(i)
        if len(pixel) == 3:
            row.insert(0,pixel)
            pixel = []
        if len(row) == int(w):
            newBody.append(row)
            row = []
    print("Match confirm: reflex matrix created successfully")

    # La paso nuevamente a formato entero de lista

    for i in newBody:
        for j in i:
            for y in j:
                finalList.append(y)
    print("Match confirm: new reflex body created")
    return finalList
 
# Ejecuto funciones creadas para generar el header y las colas de colores y full color, asi como obtener
# los valores del header para su uso correspondiente 
                
arguments = parser.parse_args()
image = open(arguments.fileImage, 'rb')

form,width,height,maxCol = Header(image)     


newHeaderRotated = RemakingHeader(form,width,height,maxCol,arguments.rotation,False)
newHeaderNotRotated = RemakingHeader(form,width,height,maxCol,False,arguments.mirror)
pixelsRed,pixelsGreen,pixelsBlue,pixelsImg = Body(image,arguments.size)




# Se crean y ejecutan los hilos, los cuales son opcionales, 4 para rotacion y 4 para reflexcion 


if(arguments.rotation == True):

    threadRedRotated = threading.Thread(target=ImageProcessing,args=((arguments.fileImage,pixelsRed,'red',arguments.red,maxCol,newHeaderRotated,newHeaderNotRotated,arguments.rotation,False,width,height)))
    threadGreenRotated = threading.Thread(target=ImageProcessing,args=((arguments.fileImage,pixelsGreen,'green',arguments.green,maxCol,newHeaderRotated,newHeaderNotRotated,arguments.rotation,False,width,height)))
    threadBlueRotated = threading.Thread(target=ImageProcessing,args=((arguments.fileImage,pixelsBlue,'blue',arguments.blue,maxCol,newHeaderRotated,newHeaderNotRotated,arguments.rotation,False,width,height)))
    threadFullColourRotated = threading.Thread(target=ImageProcessing,args=((arguments.fileImage,pixelsImg,'colour',arguments.colour,maxCol,newHeaderRotated,newHeaderNotRotated,arguments.rotation,False,width,height)))

    threadRedRotated.start()
    threadGreenRotated.start()
    threadBlueRotated.start()
    threadFullColourRotated.start()

        

if(arguments.mirror == True):

    threadRedMirror = threading.Thread(target=ImageProcessing,args=((arguments.fileImage,pixelsRed,'red',arguments.red,maxCol,newHeaderRotated,newHeaderNotRotated,False,arguments.mirror,width,height)))
    threadGreenMirror = threading.Thread(target=ImageProcessing,args=((arguments.fileImage,pixelsGreen,'green',arguments.green,maxCol,newHeaderRotated,newHeaderNotRotated,False,arguments.mirror,width,height)))
    threadBlueMirror = threading.Thread(target=ImageProcessing,args=((arguments.fileImage,pixelsBlue,'blue',arguments.blue,maxCol,newHeaderRotated,newHeaderNotRotated,False,arguments.mirror,width,height)))
    threadFullColourMirror = threading.Thread(target=ImageProcessing,args=((arguments.fileImage,pixelsImg,'colour',arguments.colour,maxCol,newHeaderRotated,newHeaderNotRotated,False,arguments.mirror,width,height)))

    threadRedMirror.start()
    threadGreenMirror.start()
    threadBlueMirror.start()
    threadFullColourMirror.start()

# Se espera a que los hilos terminen su ejecucion para continuar con el hilo principal del programa 
    
threadRedMirror.join()
threadGreenMirror.join()
threadBlueMirror.join()
threadFullColourMirror.join()
threadRedRotated.join()
threadGreenRotated.join()
threadBlueRotated.join()
threadFullColourRotated.join()