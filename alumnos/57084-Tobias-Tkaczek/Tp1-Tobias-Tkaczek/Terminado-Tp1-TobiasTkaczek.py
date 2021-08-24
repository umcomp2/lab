import argparse
from os import path
import re
import multiprocessing as mp
import time



parser = argparse.ArgumentParser(description="Image processing")

parser.add_argument('-f','--fileImage',
required=True,
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
default=2,
type=float,
help='intensity of green')

parser.add_argument('-b','--blue',
default=0.5,
type=float,
help='intensity of blue')


def Header(file):
    aux = 0
    flag1 = False
    flag2 = False
    while(aux != 10):
        line = file.readline().splitlines()[0]
        coment = re.search(b'#',line)
        if(coment != None):
            aux = aux + 1
            continue
        if(line == b'P6'):
            flag1 = True
            form = line
            aux = aux +1
            continue
        if(flag1):
            flag2 = True
            width,height = line.split()
            flag1 = False
            aux = aux +1
            continue
        if(flag2):
            maxCol = line
            aux = aux +1
            break
    return form, width, height, maxCol             
        
        
def Body(file,size):
    forPipeRed = []
    forPipeGreen = []
    forPipeBlue = []
    pixelCant = int(width)*int(height)
    f1,f2,f3 = True,False,False
    while(len(forPipeRed) != pixelCant or len(forPipeGreen) != pixelCant or len(forPipeBlue) != pixelCant):
        byteRead = file.read(size)
        for f in byteRead:
            if(f1):
                if(len(forPipeRed) == pixelCant):
                    continue
                forPipeRed.append(f)
                f1 = False
                f2 = True
                continue
            if(f2):
                forPipeGreen.append(f)
                f2 = False
                f3 = True
                continue
            if(f3):
                forPipeBlue.append(f)
                f3 = False
                f1 = True
                continue    
    return forPipeRed,forPipeGreen,forPipeBlue

def ImageProcessing(name,pixels,colour,multiplier,maxCol,header):
    newImageBody = []
    for i in pixels.get():

        finalPixel = multiplier*i
        finalPixel = int(min(max(finalPixel,0),int(maxCol)))
          


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
    if colour == "red":
        NewImageMaker(name,"red",newImageBody,header)
    if colour == "green":
        NewImageMaker(name,"green",newImageBody,header)
    if colour == "blue":
        NewImageMaker(name,"blue",newImageBody,header)        

def NewImageMaker(name,colour,newImageBody,header):
    finalImage = open(f'{colour}_{name}','wb')
    finalImage.write(header)
    finalImage.write(bytes(newImageBody))
     

def RemakingHeader(form,width,height,maxCol):
    newHeader = b''.join((form,b'\n',width,b' ',height,b'\n',maxCol,b'\n'))
    return newHeader


                
arguments = parser.parse_args()
image = open(arguments.fileImage, 'rb')

form,width,height,maxCol = Header(image)     


newHeader = RemakingHeader(form,width,height,maxCol)
pixelsRed,pixelsGreen,pixelsBlue = Body(image,arguments.size)

cola = mp.Queue()

cola.put(pixelsRed)
cola.put(pixelsGreen)
cola.put(pixelsBlue)

hijo1 = mp.Process(target=ImageProcessing, args=(path.basename(arguments.fileImage),cola,"red",arguments.red,maxCol,newHeader))
hijo2 = mp.Process(target=ImageProcessing, args=(path.basename(arguments.fileImage),cola,"green",arguments.green,maxCol,newHeader))
hijo3 = mp.Process(target=ImageProcessing, args=(path.basename(arguments.fileImage),cola,"blue",arguments.blue,maxCol,newHeader))

hijo1.start()
hijo2.start()
hijo3.start()

hijo1.join()

hijo2.join()

hijo3.join()


time.sleep(1)
print('.....33%.....')
time.sleep(1)
print('.....66%.....')
time.sleep(1)
print('.....99%.....')


print("finish")
print(image.read(3))