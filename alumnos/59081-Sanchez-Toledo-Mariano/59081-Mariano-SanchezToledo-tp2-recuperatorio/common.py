from threading import Semaphore
from parse import Parser
from Input import Input

args = Parser.parser()
fileInp = args.file
file = Input(fileInp)
header, column, row = file.processImage()
sem = Semaphore(3)