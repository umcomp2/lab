import os
import sys
import array
import matplotlib.pyplot as plot

def histo (cola,color,archivo,geometria,bonus):

    width, height, maxval = geometria
    len_total = 0
    histo = [0] * (maxval + 1) #there are 256 posibilities, not 255
    while len_total < (width * height * 3):
        leido = cola.get()
        print ( "lee de a bloques" ,  len(leido)) 
        len_total = len_total + len(leido)
        offs = {'r':0, 'g':1 , 'b':2}
        for x in range(0, len(leido),3):
            index =  x + offs[color]
            histo[leido[index]] = histo[leido[index]] + 1
    #print (color, histo)
    plot.plot(range(0,256),histo)
    titulo =  "Histograma {}:".format(color.upper())
    plot.title(titulo)
    plot.xlabel("Intensidad color")
    plot.ylabel("Frecuencia")
    plot.grid(True)
    plot.xticks(range(0,257,16))
    plot.savefig(color + '_' + archivo + '.png')
    plot.show()
    original_stdout = sys.stdout
    fd = open(color + '_' + archivo + '.txt', 'w')
    sys.stdout = fd
    for i in range(len(histo)):
        print (i , '\t' , histo[i] )
    sys.stdout = original_stdout
    fd.close()

