from os import remove
from queue import *
from Input import is_eof


def processList(filename="body.tmp"):
    rq = Queue()
    gq = Queue()
    bq = Queue()
    with open(filename, 'rb') as fd:
        pointer = -1
        while True:
            pointer +=1
            if pointer % 3 == 0:
                byte = fd.read(1)
                rq.put(byte)
                if is_eof(fd):
                    break
            elif pointer % 3 == 1:
                byte = fd.read(1)
                gq.put(byte)
                if is_eof(fd):
                    break
            elif pointer % 3 == 2:
                byte = fd.read(1)
                bq.put(byte)
                if is_eof(fd):
                    break
            elif is_eof(fd):
                break
        fd.close()
    remove(filename)
    print("Queues Done!")
    return rq, gq, bq
    

    