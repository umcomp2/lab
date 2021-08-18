import argparse, sys,os, array,time
from os.path import getsize
import multiprocessing as mp

class InvalidFormat(Exception):
    def __init__(self, message):
        print(message)

class NoFile(Exception):
    def __init__(self, message):
        print(message)

class NoNumber(Exception):
    def __init__(self,message):
        print(message)


def this_analize_the_raw_image(image,size):
    raw_data =[]
    #Here i put the data in blocks of -s  and then separet the individual values
    for iterador in range (int(getsize(image)/size)):
        raw_data.append(os.read(image,size))

    raw_data.append(os.read(image,(getsize(image)%size)))
    raw_data = b''.join(raw_data)
 

    global header
    global body

    #Here i strip the comments
    for i in range(raw_data.count(b"\n# ")):
        coments1 = raw_data.find(b"\n# ")
        coments2 = raw_data.find(b"\n", coments1 + 1)
        raw_data = raw_data.replace(raw_data[coments1:coments2], b"")
    

    #Here i change every value expresed as bit to a integers in a list
    header_finder = raw_data.find(b"\n", raw_data.find(b"\n", raw_data.find(b"\n") +1) +1) +1
    header = raw_data[:header_finder].decode()    #nesesary express the header to decode the image
    body = raw_data[header_finder:]
    data_procesed = [i for i in body]

    #create a list of list, where every 3 values(rgb) append as a list in the main list
    pixel_data = []
    while len(data_procesed)>3:
        pice = data_procesed[:3]
        pixel_data.append(pice)
        data_procesed=data_procesed[3:]

    #take the header and transform it into a list to take the rows and colums(of pixels) of the image nota:como es global el header puede ir en otro lado
    li = (list(header.split("\n")))[1].split(" ")
    row = int(li[0])
    column = int(li[1])
    
    return pixel_data,row,column

def main():
    parser = argparse.ArgumentParser(usage="\nTP_agus.py [-h] [-s SIZE] [-f FILE]")
    parser.add_argument('-s', '--size', metavar='SIZE', type=int,default=1024, help="Lecture Block size")
    parser.add_argument('-f', '--file', metavar='FILE', type=str,help="image .ppm to process")
    args = parser.parse_args()
    file = args.file
    size = args.size
    q = mp.Queue()

    if not file.endswith(".ppm"):
        raise InvalidFormat("image is an invalid format, must be .ppm")
        
    if not file:
        raise NoFile("No file entered, check -h")

    if (type(size) !=  int) or (size< 0):
        raise NoNumber("You must enter positive integer number with -s ")

    try:
        image= os.open(file, os.O_RDONLY)
        namefile = file.replace('.ppm','')

    except NoFile:
        print(" No such file or directory: '"+ file +"'")
        sys.exit()

    pixel_data,row,column = this_analize_the_raw_image(image,size)

    os.close(image)
    rotated=[]
    cant_columnas = column

    for x in range (column):
        for y in range(row):
            rotated.append(pixel_data[y][cant_columnas])
        cant_columnas = cant_columnas -1
    
    flat_list =[item for sublist in rotated for item in sublist]


    archivo= array.array('B',flat_list)

    with open(f'rotated.ppm', 'wb') as f:
        f.write(bytearray(header, 'ascii'))
        archivo.tofile(f)
    
    


    """#esta partede codigo convierte mi lista de listas en una lista de valores para asi poder crear la imagen
    pixel_data=pixel_data[::-1]
    flat_list =[item for sublist in pixel_data for item in sublist]


    archivo= array.array('B',flat_list)

    with open(f'rotated.ppm', 'wb') as f:
        f.write(bytearray(header, 'ascii'))
        archivo.tofile(f)
    #--------------------------------------------------------------------
    """

if __name__ == "__main__":
    main()
    