import os
from parse import Parser
from Input import Input




args = Parser.parser()
fileInp = args.file

image = Input(fileInp)
header = image.getHeader()
image.getBody()

with open('test2.ppm', 'wb',os.O_CREAT) as fd:
    fd.write(header)
    fw = open('temp.tmp', 'rb')
    data = fw.read()
    fd.write(data)