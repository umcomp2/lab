#!/usr/bin/env python
import os
import sys
import signal
import time

T = 1

def SIGUSR2_handler(signum, frame):
    global T
    T /= 2
    if T < 1:
        print("...Terminando programa (lapso menor a 1 segundo)")
        sys.exit(0)

def SIGUSR1_handler(signum, frame):
    global T
    T *= 2

if __name__ == "__main__":
    signal.signal(signal.SIGUSR2, SIGUSR2_handler)
    signal.signal(signal.SIGUSR1, SIGUSR1_handler)
    print(os.getpid())
    i = 0
    while True:
        print("contador: %d\tlapso: %d" % (i, T))
        i += 1
        time.sleep(T)
