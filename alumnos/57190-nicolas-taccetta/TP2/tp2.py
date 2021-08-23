import os
import argparse
import threading
import time
import array
import sys
from concurrent.futures import ThreadPoolExecutor as TPE

def image_reader(imagefile):

    text = f"Parent Process ID {os.getpid()} reading file..."
    load_animation(text, 0.005)

    global header
    global body

    global width
    global height

    try:
        #Comments deleter
        for i in range(imagefile.count(b"\n# ")):
            coments1 = imagefile.find(b"\n# ")
            coments2 = imagefile.find(b"\n", coments1 + 1)
            imagefile = imagefile.replace(imagefile[coments1:coments2], b"")
        
        #Formating image to int
        header_finder = imagefile.find(b"\n", imagefile.find(b"\n", imagefile.find(b"\n") +1) +1) +1
        header = imagefile[:header_finder].decode()
        body = imagefile[header_finder:]
        processimage = [i for i in body]

        #rotacion header
        space = header.find(' ')
        word1 = header.replace("P6\n", "")
        word1 = word1.replace(header[space:], "")
        word2 = header.replace("P6\n", "")
        word2 = word2.replace(word1+" ", "")
        jumping2 = word2.find("\n")
        word3 = word2.replace(word2[:jumping2], "")
        word2 = word2.replace(word2[jumping2:], "")
        word3 = word3.replace("\n", "")

        height = int(word2)
        width = int(word1)

        print(width, height)

        """header = header.replace(word1, word2)
        header = header.replace(" "+word2, " "+word1)
        print(header)"""

        """def invertirMatriz():
        for y in matrix:
            y.reverse()
        return matrix"""

        #print(header[space:] + " " + header[:space])

        return processimage

    except:
        print("Error(1): Incorrect path or corrupt data file (must be bytes)")
        exit(3)

def creatergb(ppmread,rgb):
    #Auxiliar variables
    
    large = len(ppmread)
    g = -2
    b = -1
    r = 0
    filename = args.file.replace('.ppm', '')
    #red creator
    if rgb == 0:
        ppmr = ppmread.copy()
        position = 0
        name = histo_name = "red_filter_" + filename
        for i in range(large):
            g = g + 3
            b = b + 3
            if g < large:
                ppmr[g] = 0
            if b < large:
                ppmr[b] = 0
        print("Red Processed")

        candle.acquire()
        pixelsrgb = width * height * 3
        pixelwidth = width * 3

        listarev = [0] * pixelsrgb
        pixelsrgb = pixelsrgb - 1
        pixel = width * 3 - 1
        pixelpunt = pixel

        pix = 0
        pixelcount = 1

        for i in range(height):
            
            for j in range(width):
                listarev[pix] = ppmr[pixel-2]
                listarev[pix+1] = ppmr[pixel-1]
                listarev[pix+2] = ppmr[pixel]
                pix = pix + 3
                pixel = pixel - 3

            pixelcount = pixelcount + 1
            pixel = pix + pixelpunt

        ppmr = listarev
        candle.release()
        
        time.sleep(0.5)
        plot_image(ppmr, name)

    #green creator
    elif rgb == 1:

        ppmg = ppmread.copy()
        position = 1
        name = histo_name = "green_filter_" + filename
        for i in range(large):
            r = r + 3
            b = b + 3
            if r < large:
                ppmg[r] = 0
            if b < large:
                ppmg[b] = 0
        print("Green processed")


        candle.acquire()
        pixelsrgb = width * height * 3
        pixelwidth = width * 3

        pixelsrgb = pixelsrgb - 1
        pixel = width * 3 - 1
        pixelpunt = pixel

        pix = 0
        pixelcount = 1
        for i in range(height):
            
            for j in range(width):
                listarev[pix] = ppmg[pixel-2]
                listarev[pix+1] = ppmg[pixel-1]
                listarev[pix+2] = ppmg[pixel]
                pix = pix + 3
                pixel = pixel - 3

            pixelcount = pixelcount + 1
            pixel = pix + pixelpunt 
        ppmr = listarev   
        candle.release()    
        
        plot_image(ppmg, name)

    #blue creator
    elif rgb == 2:

        ppmb = ppmread.copy()
        position = 2
        name = histo_name = "blue_filter_" + filename
        for i in range(large):
            r = r + 3
            g = g + 3
            if r < large:
                ppmb[r] = 0
            if g < large:
                ppmb[g] = 0
        print("Blue Processed")



        plot_image(ppmb, name)

    print("Filter created.")

    #launch plot image
    
    

def plot_image(ppmrgb, name):
    
    print("Launching plot image.")

    #creating ppm filter
    try:
        filter_rgb = array.array('B', [i for i in ppmrgb])
        with open(name + ".ppm", "wb", os.O_CREAT) as asing:
            asing.write(bytearray(header, 'ascii'))
            filter_rgb.tofile(asing)
            asing.close()
    
    except:
        print("Error: Can't create image.")
        exit(2)
    
    print("PPM files whit RGB filters created.")

#Decorative animation        
def load_animation(text, t):
    # String to be displayed when the application is loading
    load_str = text
    ls_len = len(load_str)

    # String for creating the rotating line
    animation = "|/-\\"
    #duration
    anicount = counttime = 0
    #pointer       
    i = 0                     
    while (counttime != 100):
        # animation speed
        # smaller the value, faster will be the animation
        time.sleep(t) 
        load_str_list = list(load_str) 
        # x->obtaining the ASCII code
        x = ord(load_str_list[i])
        # y->for storing altered ASCII code
        y = 0                             
        # switch uppercase to lowercase and vice-versa 
        if x != 32 and x != 46:
            if x > 47 and x < 58:
                y = x
                pass           
            elif x>90:
                y = x-32
            else:
                y = x + 32
            load_str_list[i]= chr(y)
        # for storing the resultant string
        res =''             
        for j in range(ls_len):
            res = res + load_str_list[j]
        # displaying the resultant string
        sys.stdout.write("\r"+res + animation[anicount])
        sys.stdout.flush()
        # Assigning loading string to the resultant string
        load_str = res
        anicount = (anicount + 1)% 4
        i =(i + 1)% ls_len
        counttime = counttime + 1
    else:
        print("\n")
        #os.system("clear")


if __name__ == "__main__":
    text1 = "Iniciating program"

    #Synchro
    candle = threading.Lock()

    #Launch arguments
    try:
        parser = argparse.ArgumentParser(description='Processing PPM File')
        parser.add_argument('-f', '--file', help='File name')
        parser.add_argument('-s', '--size', type=int, help='Reading block size', default="1024")
        args = parser.parse_args()

        if args.file == None:
            print("Must specify a .ppm file")
            exit(2)
    
        if args.size == None:
            print("Must specify a reading block size")
            exit(2)  

    except:
        print("Error: Invalid Arguments.")
        exit(2)

    load_animation(text1, 0.01)
    #Open file and reading by blocks
    try:
        ppm = os.open(args.file, os.O_RDONLY)
    except:
        print("Error: No such file or directory: '"+ args.file +"'")
        exit(2)
    
    print("Opening file...")
    time.sleep(0.5)

    byt = os.stat(ppm).st_size #cuenta bytes
    rest = byt % args.size
    byt = byt // args.size
    ppm_raw = []
    for i in range(byt):
        ppm_raw.append(os.read(ppm,args.size))
    ppm_raw.append(os.read(ppm,rest))
    ppm_raw = b''.join(ppm_raw)

    print("Processing raw data...")
    time.sleep(0.5)
    #Process raw data
    ppm_image = image_reader(ppm_raw)
    os.close(ppm)
    print("File ready...")
        
    print("Launch threading...")
    time.sleep(0.5)
    
    with TPE(max_workers=3) as executor: 
        executor.map(creatergb(ppm_image, 0))
        executor.map(creatergb(ppm_image, 1))
        executor.map(creatergb(ppm_image, 2))

    """threads = list()
    for i in range(3):
        t = threading.Thread(target=creatergb(ppm_image, i))
        threads.append(t)
    
    for t in threads:
        t.start()

    for t in threads:
        t.join()"""

    exit(2)
