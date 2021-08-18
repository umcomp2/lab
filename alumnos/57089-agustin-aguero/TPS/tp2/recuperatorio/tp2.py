import argparse, sys,os, array,time
from os.path import getsize
import concurrent.futures

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
    return data_procesed


#in the header(str) search the width and height(list) and put it into variables
def width_height():
    row_and_column = (list(header.split('\n')))[1].split(' ')
    width = int(row_and_column[0])
    height = int(row_and_column[1])
    return width , height



#the data list goes into a list of list(rows) of list(pixels)
def create_a_list_of_list(data_procesed,row,column):


    index = 0
    list_of_list = []
    list_of_list_of_list = []

    while index < (len(data_procesed)-2):
        list_of_list.append(data_procesed[index:index+3])
        index +=3
    
    for f in range(0,(len(list_of_list)-1),column):
        list_of_list_of_list.append(list_of_list[f:f+column])

    return list_of_list_of_list



#first row last column to first row first column, first row second to last column to first row second column....
#  a b c d              d c b a         
#  e f g h  ---->       h g f e         #every letter is a pixel
#  i j k l              l k j i
def invert_the_list_of_list_of_list(list_of_list_of_list):
    list_inverted = []

    for f in range (len(list_of_list_of_list)):

        for c in range ((len(list_of_list_of_list[f])-1),-1,-1):

            list_inverted.append(list_of_list_of_list[f][c])

    return list_inverted


#take a list of lists of lists and output a list

def create_flat_list(list_inverted,rgb):
#def create_flat_list(list_inverted):
#    flat_list = []
#    for filas in list_inverted:
#        for pixeles in filas:
#            flat_list.append(pixeles)
#    return flat_list
    
    
    flat_list = []
    
    for filas in list_inverted:
            if rgb == 0:
                flat_list.append(filas[rgb])

            elif rgb == 1:

                flat_list.append(filas[rgb])

            elif rgb == 2:
                flat_list.append(filas[rgb])
    
    return flat_list

def union_list(data_procesed,red_list,green_list,blue_list):
    complete_list = []
    count = 0
    while (len(complete_list)) != (len(data_procesed)-1):
        complete_list.append(red_list[count])
        complete_list.append(green_list[count])
        complete_list.append(blue_list[count])
        count += 1
    return complete_list
    








#take a list, transform it into bits and write in in a .ppm file
def create_image_inverted(list_inverted,namefile):

    archivo= array.array('B',list_inverted)

    with open(f'{namefile}_mirror.ppm', 'wb') as f:
        f.write(bytearray(header, 'ascii'))
        archivo.tofile(f)
    
    print(f" image of mirror {namefile} created")


#calculate te rgb to make it into grayscale and put it into a list
def grayscale(flat_list,namefile):
    black_white = []
    r = 0
    g = 1
    b = 2
    for elements in range (0,int((len(flat_list))/3)):
        sum = int((flat_list[r])*0.3) + int((flat_list[g])*0.59) + int((flat_list[b])*0.11)
        for rep in range (0,3):
            black_white.append(sum)
        r += 3
        g += 3
        b += 3
    namefile = namefile+'_greyscale'    
    create_image_inverted(black_white,namefile)    





if __name__ == '__main__':
    start = time.perf_counter()
    parser = argparse.ArgumentParser(usage="\nTP_agus.py [-h] [-s SIZE] [-f FILE] [-bw BLACKWHITE]")
    parser.add_argument('-s', '--size', metavar='SIZE', type=int,default=1024, help="Lecture Block size")
    parser.add_argument('-f', '--file', metavar='FILE', type=str,help="image .ppm to process")
    parser.add_argument('-bw', '--blackwhite', metavar='BLACKWHITE', type=bool,default=False, help=' if -bw True:  Create a black and white image')
    args = parser.parse_args()
    file = args.file
    size = args.size
    blackwhite = args.blackwhite

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

    data_procesed = this_analize_the_raw_image(image,size)

    os.close(image)
    
    #aca consigo la cant de filas y columnas
    column, row = width_height()

    #creo una lista de listas que sera de la misma cant que la cant de filas que tiene la imagen
    #y cada fila tiene listas de a 3 elementos que seran los pixeles
    list_of_list_of_list= create_a_list_of_list(data_procesed,row,column)

    #pongo el ultimo pixel de la fila uno en primero, el penultimo de la fila uno en segundo y asi
    list_inverted = invert_the_list_of_list_of_list(list_of_list_of_list)

    #lo trasformo a una lista plana para poder escribirla en un archivo .ppm
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f_red = executor.submit(create_flat_list,list_inverted,0)
        f_green = executor.submit(create_flat_list,list_inverted,1)
        f_blue = executor.submit(create_flat_list,list_inverted,2)

        red_list = f_red.result()
        green_list = f_green.result() 
        blue_list = f_blue.result()

    complete_list =union_list(data_procesed,red_list,green_list,blue_list)

    create_image_inverted(complete_list,namefile)

    #flat_list = create_flat_list(list_inverted)

    #escribo el archivo .ppm
    #create_image_inverted(flat_list,namefile)

    #take te mirror image and modify it into greyscale
    if blackwhite == True:
        grayscale(complete_list,namefile)
    
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start,2)} second(s)')

    


