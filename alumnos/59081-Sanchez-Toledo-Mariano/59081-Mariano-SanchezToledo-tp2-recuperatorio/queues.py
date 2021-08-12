from os import remove
from queue import *
from Input import is_eof


def createQueue():
    return Queue()

def putInQueue(q, item, block = False):
    return q.put(item, block)

def queueIsEmpty(q):
    return q.empty()

def processQueue(qr, qg, qb, filename="body.tmp"):
    with open(filename, 'rb') as fd:
        pointer = -1
        while True:
            pointer +=1
            if pointer % 3 == 0:
                byte = fd.read(1)
                putInQueue(qr, byte)
                if is_eof(fd):
                    break
            elif pointer % 3 == 1:
                byte = fd.read(1)
                putInQueue(qg, byte)
                if is_eof(fd):
                    break
            elif pointer % 3 == 2:
                byte = fd.read(1)
                putInQueue(qb, byte)
                if is_eof(fd):
                    break
            elif is_eof(fd):
                break
        fd.close()
    remove(filename)
    

    