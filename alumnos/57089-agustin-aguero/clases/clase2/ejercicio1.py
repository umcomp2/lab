"""
1 - Modifique el programa visto en clases calc.py utilizando el modulo getopt :

Ejemplo de funcionamiento

# ./calc-getopt.py -h
Usage: ./calculo.py [s|r|m|d] arg1 arg2  

Mandatory ad excluyent arguments are [s|r|m|d]
  -s         suma arg1 + arg2
  -r         resta arg1 + arg2
  -m         multiplica arg1 * arg2
  -d         divide arg1 / arg2 

type  value:
   int
   float
   real

   -h, --help       print this help
"""
"""
#------EL PROGRAMA calc.py es el siguiente----------------------------------------------------------------------
#!/usr/bin/python3
import sys
#print sys.argv
operacion=False
if len (sys.argv) != 4:
    print ("Error: uso " + sys.argv[0] + " nro [s|r|d|m|p] nro")
    sys.exit()

if  sys.argv[1].isdigit() != True:
    print ("Error: uso " + sys.argv[0] + " nro [s|r|d|m] nro")
    sys.exit()
else:
    operador1 = int (sys.argv[1])
if  sys.argv[3].isdigit() != True:
    print ("Error: uso " + sys.argv[0] + " nro [s|r|d|m|p] nro")
    sys.exit()
else:
    operador2 = int (sys.argv[3])
for letra in "s" "r" "m" "d" "p":
    if letra == sys.argv[2]:
        operacion = True

if  operacion != True:
    print ("Error: uso " + sys.argv[0] + " nro [s|r|d|m|p] nro")
    sys.exit()

if sys.argv[2] == "s":
    print (operador1 + operador2)
elif sys.argv[2] == "r":
    print (operador1 - operador2)
elif sys.argv[2] == "m":
    print (operador1 * operador2)
elif sys.argv[2] == "d":
    print (operador1 / operador2)
elif sys.argv[2] == "p":
    print (operador1 ** operador2)
#-----------------------------------------------------------------------------------------------------------
"""
import sys
import getopt

def main():
    #args = sys.argv[1:]   # esto va a guardar en una variable los argumentos de entrada omitiendo la posicion cero que sera el nombre del archivo .py que estamos usando
    #print(f"entrada:\n{args}")
    ayuda = """Usage: ./calculo.py [s|r|m|d] arg1 arg2  

    Mandatory ad excluyent arguments are [s|r|m|d]
    -s         suma arg1 + arg2
    -r         resta arg1 + arg2
    -m         multiplica arg1 * arg2
    -d         divide arg1 / arg2 

    type  value:
    int

    -h, --help       print this help"""

    opciones , args = getopt.getopt(sys.argv[1:], "srmdph")
    print(f"argumentos:\n{args}")
    print(f"opciones:\n{opciones}")
    for elementos in args:
        if elementos.isdigit() != True:
            print("los argumentos a operar no son numeros")
            sys.exit()

    for tuplas in opciones:
        if tuplas[0] == "-h":
            print(ayuda)
            sys.exit()
        if tuplas[0] == "-s":
            suma = 0
            for elementos in args:
                suma = suma + int(elementos)
            print(f"suma:\n{suma}")
        if tuplas[0] == "-r":
            print(f"resta:\n{int(args[0])-int(args[1])}")
        
        if tuplas[0] == "-m":
            print(f"multiplicacion:\n{int(args[0])*int(args[1])}")

        if tuplas[0] == "-d":
            print(f"divicion:\n{int(args[0])/int(args[1])}")
        
        if tuplas[0] == "-p":
            print(f"potencia:\n{int(args[0])**int(args[1])}")

if __name__ == "__main__":
    main()