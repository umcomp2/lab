from common import *
from os import remove
from queue import *
from Input import is_eof


def processQueue(rq, gq, bq, filename="body.tmp"):
    try:
        with open(filename, 'rb') as fd:
            pointer = -1
            while True:
                if rq.empty() and gq.empty() and bq.empty():
                    sem.acquire()
                    for i in range(size):
                        pointer +=1
                        if pointer % 3 == 0:
                            print('red')
                            byte = fd.read(1)
                            rq.put(byte)
                            if is_eof(fd):
                                break
                        elif pointer % 3 == 1:
                            print('green')
                            byte = fd.read(1)
                            gq.put(byte)
                            if is_eof(fd):
                                break
                        elif pointer % 3 == 2:
                            print('blue')
                            byte = fd.read(1)
                            bq.put(byte)
                            if is_eof(fd):
                                break
                        elif is_eof(fd):
                            break
                    print(rq.qsize(), gq.qsize(), bq.qsize())
                    sem.release()
                
                elif is_eof(fd):
                    break
                
                else:
                    continue

        fd.close()
        remove(filename)
        return rq, gq, bq
    except:
        raise RuntimeError('Error al cargar queues')
    

    