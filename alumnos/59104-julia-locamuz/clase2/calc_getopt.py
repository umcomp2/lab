#!/usr/bin/python3

import sys, getopt


argv = sys.argv[1:]
print('argumentos: ' , argv)


def calc(opciones, argumentos):
    if len(opciones) == 1:
        if len(argumentos) == 2:
            if opciones[0][0] == '-s':
                print('suma')
                print(int(argumentos[0]) + int(argumentos[1]))
                
            if opciones[0][0] == '-r':
                print('resta')
                print(int(argumentos[0]) - int(argumentos[1]))

            if opciones[0][0] == '-m':
                print('multiplicacion')
                print(int(argumentos[0]) * int(argumentos[1]))

            if opciones[0][0] == '-d':
                print('division')
                print(int(argumentos[0]) / int(argumentos[1]))
        elif opciones[0][0] == '-h':
            print('''Usage: ./calculo.py [s|r|m|d] arg1 arg2  

                        Mandatory ad excluyent arguments are [s|r|m|d]
                        -s         suma arg1 + arg2
                        -r         resta arg1 + arg2
                        -m         multiplica arg1 * arg2
                        -d         divide arg1 / arg2 

                        type  value:
                        int
                        float
                        real 
                ''')
        else: 
            raise ValueError

  

def main():
    try: 
        opciones, argumentos = getopt.getopt(argv, 'srmdh')
        print(opciones, argumentos)
        calc(opciones, argumentos)
        
    except Exception as err:
        print(err + str(err))
        sys.exit(1)

if __name__ == '__main__':
    main()