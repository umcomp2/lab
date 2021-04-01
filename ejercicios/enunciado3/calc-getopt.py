#!/usr/bin/python3
import sys
import getopt


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   'srmdph', 
                                   ["suma", "resta", "multiplicacion", "division", "ptencia", "help"])
    except getopt.GetoptError as err:
        print(err)
        ayuda()         # Muestra una ayuda(help)
        sys.exit(2)     # Salida por error

    for i in range(len(args)):
        args[i] = float(args[i])

    for option in opts:
        if option[0] in ("-h", "--help"):
            ayuda()
        elif option[0] in ("-s", "--suma"):
            print(args[0] + args[1])
        elif option[0] in ("-r", "--resta"):
            print(args[0] - args[1])
        elif option[0] in ("-m", "--multiplicacion"):
            print(args[0] * args[1])
        elif option[0] in ("-d", "--division"):
            print(args[0] / args[1])
        elif opcion[0] == ("-p", "--potencia"):
            print(args[0] ** args[1])
        else:
            ayuda()
            sys.exit(1)     
        sys.exit(0)         


def ayuda():
    print("")
    print("./calc-getopt.py s|r|m|d|p arg1 arg2\n")
    print("Mandatory ad excluyent arguments are [s|r|m|d]:")
    print("-s\tsuma         arg1 + arg2")
    print("-r\tresta        arg1 - arg2")
    print("-m\tmultiplica   arg1 * arg2")
    print("-d\tdivide       arg1 / arg2")
    print("\nValue type for numerical args:")
    print("int\nfloat\nreal")
    print("** Use floating point NOT COMMA **")
    print("\n\n-h --help \tprint this help")


if __name__ == '__main__':
    main()
