import re
import os

def validar_argumentos(argumento):
    if re.search(r'[a-z|A-Z|\-]', argumento) != None:
        print('ERROR: algun/os argumentos son invalidos')
        os.system('pkill -9 -f main.py')
    elif '.' in argumento:
        return float(argumento)
    else:
        return int(argumento)
