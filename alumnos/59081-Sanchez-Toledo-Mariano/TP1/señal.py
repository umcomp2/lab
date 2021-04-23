import signal
import os
import time

fd = os.open('tux.ppm', os.O_RDWR|os.O_CREAT)
fd = os.open('tuxa.ppm', os.O_RDWR|os.O_CREAT)

def handler(pid):
    os.wait()

pid1 = os.fork()

if pid1 == 0:
    signal.signal(signal.SIGUSR1)
