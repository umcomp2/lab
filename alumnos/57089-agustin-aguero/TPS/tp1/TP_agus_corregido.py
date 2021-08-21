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
    return data_procesed

def image_analizer(q,namefile,rgb):

    data_procesed = q.get()
    only_one_color = []
    actual_color = []
    if rgb == "RED":

        for j in range(0,len(data_procesed),3):
            only_one_color.append(data_procesed[j])
            actual_color.append(data_procesed[j])
            actual_color.append(0)
            actual_color.append(0)

    elif rgb == "GREEN":
        for j in range(1,len(data_procesed),3):
            only_one_color.append(data_procesed[j])
            actual_color.append(0)
            actual_color.append(data_procesed[j])
            actual_color.append(0)

    elif rgb == "BLUE":
        for j in range(2,len(data_procesed),3):
            actual_color.append(0)
            actual_color.append(0)
            actual_color.append(data_procesed[j])
            only_one_color.append(data_procesed[j])
    
    only_one_color.sort()
    color = actual_color
    color_image(rgb,color,namefile)
    dic_color = {i:only_one_color.count(i) for i in only_one_color}
    histogram(rgb,namefile,dic_color)

    
def color_image(rgb,color,namefile):

    archivo= array.array('B',color)

    with open(f'{namefile}_{rgb}.ppm', 'wb') as f:
        f.write(bytearray(header, 'ascii'))
        archivo.tofile(f)
    
    print(f"{rgb} image of {namefile} created")

def histogram(rgb,namefile,dic_color):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    writehisto = open(dir_path + '/' + namefile + "_" + rgb + "_histogram.txt", "w")
    for key , value in dic_color.items():
            writehisto.write(f"{key}̣  ____  {value}" + os.linesep)
    
    print(f"{rgb} histogram of {namefile} created")


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

    data_procesed = this_analize_the_raw_image(image,size)

    os.close(image)

    #initialize each process with his arguments
    time.sleep(1)
    print("Launching Child 1: RED")
    q.put(data_procesed)
    c1 = mp.Process(target = image_analizer, args = (q,namefile,"RED"))
    time.sleep(1)
    print("Launching Child 2:GREEN")
    q.put(data_procesed)
    c2 = mp.Process(target = image_analizer, args = (q,namefile,"GREEN"))
    time.sleep(1)
    print("Launching Child 3:BLUE")
    q.put(data_procesed)
    c3 = mp.Process(target = image_analizer, args = (q,namefile,"BLUE"))
    
    #start the process
    c1.start()
    c2.start()
    c3.start()
    #block the process

    print("This could take a while...")
    c1.join()
    c2.join()
    c3.join()

    print("all 3 child process finish")
    time.sleep(1)
    print("Killing children")

    #kill the process
    c1.terminate()
    c2.terminate()
    c3.terminate()

    time.sleep(1)
    print("\nExiting program\n")

if __name__ == "__main__":
    main()
    
