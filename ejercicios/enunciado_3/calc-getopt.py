#!/usr/bin/python3

import sys
import getopt

#print sys.argv
def main(): 
    try:

        opts, arg = getopt.getopt(sys.argv[1:],"srmdph", ["suma", "resta", "multiplicacion", "division", "potencia", "help"])
    except getopt.GetoptError as err:
        print (err) #Imprime una ayuda 
        usage()
        sys.exit(2)

    for o in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(2)
        elif o in ("-s", "--suma"):
            print(arg[0] + arg[1]) 
        elif o in ("-r", "--resta"):
            print(arg[0] - arg[1])
        elif o in ("-m", "--multiplicacion"):
            print(arg[0] * arg[1])
        elif o in ("-d", "--division"):
            print(arg[0] / arg[1])
        elif o in ("-p", "--potencia"):
            print(arg[0] ** arg[1])
        else:
            usage()
            sys.exit(2)
    

def usage():
    print(" Mandatory ad excluyent arguments are [s|r|m|d]")
    print(" -s         suma arg1 + arg2")
    print(" -r         resta arg1 + arg2")
    print(" -m         multiplica arg1 * arg2")
    print(" -d         divide arg1 / arg2")
    print(" type  value: int, float, real") 


if __name__ == '__main__':
    main()


