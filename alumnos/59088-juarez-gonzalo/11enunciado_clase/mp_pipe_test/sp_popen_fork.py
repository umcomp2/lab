import os
import sys

from subprocess import Popen, PIPE

from time import sleep

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: %s [int]" % __file__)
        sys.exit(1)
    lapse = int(sys.argv[1])

    # sin stdout=PIPE no se crea el FIFO (medio obvio pero bueno)
    #p = Popen(["sleep", "%i" % lapse])
    p = Popen(["sleep", "%i" % lapse], stdout=PIPE)
    print("child pid %i" % p.pid, flush=True)
    print("parent pid %i" % os.getpid(), flush=True)

    p.wait()
    print("child reap-parent sleep")

    # si se usa PIPE en el constructor entonces el pipe sobrevive incluso
    # despues de reapear el proceso hasta llamar communicate()
    sleep(lapse)
    p.communicate()
    print("parent call child.communicate()-parent sleep")
    sleep(lapse)

    print("parent exit")
    sys.exit(0)
