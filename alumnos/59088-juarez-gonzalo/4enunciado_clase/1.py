#!/usr/bin/env python3
import os
import sys
import getopt

import signal
import time

CMD = "ps"
ARGS = ["-f"]
SLEEPTIME = 3600

def SIGUSR1_handler(signum, frame):
    try:
        print("SIGUSR1_handler")
        while os.wait():
            continue
    except ChildProcessError as err:
        # print("exception")
        if err.errno == 10:
            # exec no implica flush de stdout (se pierde output si lo hay)
            sys.stdout.flush()
            os.execvp(CMD, ARGS)

def usagendie():
    print("Usage: %s -c <num>" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    try:
        signal.signal(signal.SIGUSR1, SIGUSR1_handler)

        opt, args = getopt.getopt(sys.argv[1:], "c:")
        if len(opt) < 1 or len(opt[0]) < 1:
            raise ValueError()
        cnum = int(opt[0][1])

        # sin flush: python intenta buffear antes de escribir a stdout
        # por CoW el hijo solo va a reservar memoria cuando escriba al buffer.
        # el hijo al flushear escribe lo q agregó + lo del padre
        #
        # resumen: flushear lo correspondiente a un proceso para
        # consistencia en el output
        # recrear el bug: quitar flush y redirigir stdout a un archivo
        print("padre: %d" % os.getpid())
        sys.stdout.flush()

        for i in range(cnum):
            if not os.fork():
                print("\tpid hijo: %d" % os.getpid())
                sys.exit(0)
                # alternativa a sys.exit()
                #sys.stdout.flush()
                #os._exit(os.EX_OK) # no flush de buffers (acumulativo)

        signal.sigwait([signal.SIGUSR1])
    except ValueError as err:
        usagendie()
