from threading import Lock
from parse import Parser
from Input import Input


args = Parser.parser()
fileInp = args.file
file = Input(fileInp)
header, column, row = file.processImage()
matrix = [[['R', 'G', 'B'] for x in range(column)] for y in range(row)]
lock = Lock()