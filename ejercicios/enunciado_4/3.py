#!/usr/bin/python3
import time
import os
import signal

class Señal():
    def __init__(self):
        self.time = 1
        self.numero = 0

    def handler(self,signal_number,frame):
        if signal_number == 10:
            self.time = self.time * 2

        if signal_number == 12:
                self.time = self.time / 2
                if self.time  < 1:
                    exit()

    def mostrar(self):
        while True:
            self.numero += 1
            print(self.numero) #, self.time)
            time.sleep(self.time)

if __name__ == "__main__":

    def recibir_señal(signal_number,frame):
        inst.handler(signal_number, frame)

    signal.signal(signal.SIGUSR1,recibir_señal)
    signal.signal(signal.SIGUSR2,recibir_señal)

    inst=Señal()
    print(os.getpid())
    inst.mostrar()
    #Wait until a signal arrives.
    signal.pause()
