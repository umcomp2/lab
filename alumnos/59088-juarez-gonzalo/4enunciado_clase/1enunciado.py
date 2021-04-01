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
        print("recv SIGUSR1")
        while os.wait():
            continue
    except ChildProcessError as err:
        print("exception")
        if err.errno == 10:
            os.execvp(CMD, ARGS)

def usagendie():
    print("Usage: %s -c <num>" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    try:
        signal.signal(signal.SIGUSR1, SIGUSR1_handler)
        print(sys.argv)

        opt, args = getopt.getopt(sys.argv[1:], "c:")
        if len(opt) < 1 or len(opt[0]) < 1:
            raise ValueError()
        cnum = int(opt[0][1])

        print(os.getpid())
        for i in range(cnum):
            if not os.fork():
                sys.exit(666)

        time.sleep(SLEEPTIME)
    except ValueError as err:
        usagendie()
