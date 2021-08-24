import os
import argparse
import multiprocessing as mp
import time
import array
import sys

def image_reader(imagefile):
    
    text = f"Parent Process ID {os.getpid()} reading file..."
    load_animation(text, 0.05)

    global header
    global body

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

        return processimage

    except:
        print("Error(1): Incorrect path or corrupt data file (must be bytes)")
        exit(3)

def histogram(ppm,rgb):
    #Auxiliar variables
    ppm = ppm.get()
    large = len(ppm)
    g = -2
    b = -1
    r = 0
    filename = args.file.replace('.ppm', '')
    #red creator
    if rgb == "r":
        position = 0
        name = histo_name = "red_filter_" + filename
        for i in range(large):
            g = g + 3
            b = b + 3
            if g < large:
                ppm[g] = 0
            if b < large:
                ppm[b] = 0
        print("Red Processed")
        time.sleep(0.5)

    #green creator
    elif rgb == "g":
        position = 1
        name = histo_name = "green_filter_" + filename
        for i in range(large):
            r = r + 3
            b = b + 3
            if r < large:
                ppm[r] = 0
            if b < large:
                ppm[b] = 0
        print("Green processed")
        time.sleep(0.5)

    #blue creator
    elif rgb == "b":
        position = 2
        name = histo_name = "blue_filter_" + filename
        for i in range(large):
            r = r + 3
            g = g + 3
            if r < large:
                ppm[r] = 0
            if g < large:
                ppm[g] = 0
        print("Blue Processed")
        time.sleep(0.5)

    pos = position
    #color RGB position in pixel
    #Histogram sort by intensity of color
    histo = [[0] * 2 for i in range(256)]
    for color in range(256):
        histo[color][0] = color
        for i in range(0,large,3):
            if ppm[pos] == color:
                histo[color][1] = histo[color][1] + 1
            pos = pos + 3
            if pos > large-3:
                break
        pos = position

    #Creating histogram.txt
    dir_path = os.path.dirname(os.path.realpath(__file__))
    printhisto = open(dir_path + '/' + histo_name + "_histogram.txt", "w")

    try:
        printhisto.write("color      Repeats" + os.linesep)
        for i in range(len(histo)):
            if histo[i][0] < 10:
                printhisto.write("  0")
                printhisto.write(f"{histo[i][0]}̣  ____  {histo[i][1]}" + os.linesep)
            elif histo[i][0] > 9 and histo[i][0] < 100:
                printhisto.write(f"  {histo[i][0]}̣  ____  {histo[i][1]}" + os.linesep)
            else:
                printhisto.write(f" {histo[i][0]}̣  ____  {histo[i][1]}" + os.linesep)
    except:
        print("Error: Can't create histogram.")
        exit(2)

    print("Histograms created.")
    time.sleep(0.5)
    #launch plot image
    plot_image(ppm, name)
    

def plot_image(ppm, name):
    print("Launching plot image.")
    time.sleep(0.5)
    #creating ppm filter
    try:
        filter_rgb = array.array('B', [i for i in ppm])
        with open(name + ".ppm", "wb", os.O_CREAT) as asing:
            asing.write(bytearray(header, 'ascii'))
            filter_rgb.tofile(asing)
            asing.close()
    
    except:
        print("Error: Can't create image.")
        exit(2)
    
    print("PPM files whit RGB filters created.")
    time.sleep(0.5)

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
    
    #Creating Queue
    q = mp.Queue()

    #Launch arguments
    try:
        parser = argparse.ArgumentParser(description='Processing PPM File')
        parser.add_argument('-f', '--file', help='File name')
        parser.add_argument('-s', '--size', type=int, help='Reading block size')
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

    byt = os.stat(ppm).st_size
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

    print("Launch multiprocess...")
    time.sleep(2)
    #Launch childs processes.
    q.put(ppm_image)
    child_one = mp.Process(target = histogram, args = (q, "r"))
    q.put(ppm_image)
    child_two = mp.Process(target = histogram, args = (q, "g"))
    q.put(ppm_image)
    child_three = mp.Process(target = histogram, args = (q, "b"))
    
    child_one.start()
    child_two.start()
    child_three.start()
    
    child_one.join()
    child_two.join()
    child_three.join()

    print("\nExiting program\n")
    child_one.terminate()
    child_two.terminate()
    child_three.terminate()

    exit(10)
