import os
from queues import *
from common import *
from parse import Parser
from Input import Input



def main():
    file = Input(fileInp)
    header, column, row = file.getHeader()
    '''file.getBody()
    qr, qg, qb = createQueue()
    processQueue(qr, qg, qb)'''
    print(column, row)



if __name__ == "__main__":
    main()