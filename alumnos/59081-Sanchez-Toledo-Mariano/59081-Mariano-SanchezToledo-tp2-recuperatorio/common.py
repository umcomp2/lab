from threading import Lock
from parse import Parser
from Input import Input

args = Parser.parser()
fileInp = args.file
file = Input(fileInp)
size = args.size
header, column, row = file.processImage()
sem = Lock()
