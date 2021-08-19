from threading import Lock
from parse import Parser
from Input import Input


args = Parser.parser()
fileInp = args.file
file = Input(fileInp)
size = args.size
try:
    header, column, row = file.processImage()
except:
    raise ValueError('Error en ruta de imagen, verifique e intente nuevamente')
sem = Lock()
