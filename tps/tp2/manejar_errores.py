import os

def manejo_de_errores(parser, filename, size):

    # si no se ingresa el nombre de un archivo
    if not filename:
        parser.error('ERROR EN EL ARGUMENTO [-f] [--file]! No se ingreso el nombre de un archivo')

    # si el nombre del archivo no existe
    if os.path.isfile(filename):
        pass
    else:
        #raise FileNotFoundError(f'El archivo {filename} no ha sido encontrado')
        parser.error(f'ERROR EN EL ARGUMENTO [-f] [--file]! El archivo {filename} no ha sido encontrado')
    
    # si el archivo no es ppm
    if not filename.endswith(".ppm"):
        parser.error('ERROR EN EL ARGUMENTO [-f] [--file]! El archivo ingresado no es .ppm')

    # si el s ingresado es negativo
    if size < 0:
        parser.error('ERROR EN EL ARGUMENTO [-n]! El tamano del bloque a leer no puede ser un numero negativo.')