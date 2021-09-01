import os
import sys

from time import sleep

def p_sleep(lapse):
    print("child pid %i" % os.getpid(), flush=True)
    sleep(lapse)

# aca el problema de los pipes que no se cierran despues de wait() no existe
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: %s [int]" % __file__)
        sys.exit(1)
    lapse = int(sys.argv[1])
    p = os.fork()
    if not p:
        p_sleep(lapse)
    print("parent pid %i" % os.getpid(), flush=True)
    os.wait()
    print("reap")
    sys.exit(0)
