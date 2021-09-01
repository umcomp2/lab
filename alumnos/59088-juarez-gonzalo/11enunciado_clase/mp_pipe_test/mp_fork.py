import sys
import os

import multiprocessing as mp

from time import sleep

def p_sleep(lapse):
    print("\nchild pid %i @ %s\n" % (os.getpid(), __file__), flush=True)
    sleep(lapse)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nusage: %s [int] @ %s\n" % (__file__, __file__))
        sys.exit(1)
    lapse = int(sys.argv[1])

    # el constructor Process() crea el objeto Process
    # pero no el proceso desde el punto de vista del OS
    p = mp.Process(target=p_sleep, args=(lapse,))

    # p.start() crea 2 pipes para comunicacion
    # padre-hijo y luego llama os.fork() (crea el
    # proceso desde el punto de vista del OS)
    p.start()
    print("\nparent pid %i @ %s\n" % (os.getpid(), __file__), flush=True)

    # p.join() llama a wait() en el proceso hijo
    # pero no cierra los pipes (cierra el proceso desde
    # el punto de vista del OS) y setea un valor booleano
    # en el objeto Process que lo identifica como cerrado
    p.join()
    print("\nchild reap-parent sleep @ %s\n" % __file__)
    sleep(lapse)

    # p.close() limpia el objeto Process
    print("\nparent call child.close()-parent sleep @ %s\n" % __file__)
    p.close()
    sleep(lapse)

    print("\nparent exit @ %s\n" % __file__)

    sys.exit(0)
