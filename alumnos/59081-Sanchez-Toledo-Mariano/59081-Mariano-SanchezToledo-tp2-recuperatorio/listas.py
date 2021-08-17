from os import remove
from queue import *
from Input import is_eof


def processList(filename="body.tmp"):
    rlist = []
    glist = []
    blist = []
    with open(filename, 'rb') as fd:
        pointer = -1
        while True:
            pointer +=1
            if pointer % 3 == 0:
                byte = fd.read(1)
                rlist += byte
                if is_eof(fd):
                    break
            elif pointer % 3 == 1:
                byte = fd.read(1)
                glist += byte
                if is_eof(fd):
                    break
            elif pointer % 3 == 2:
                byte = fd.read(1)
                blist += byte
                if is_eof(fd):
                    break
            elif is_eof(fd):
                break
        fd.close()
    remove(filename)
    return rlist, glist, blist
    

    