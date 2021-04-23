import os
import time


fdl, fde = os.pipe()
pid1 = os.fork()

if pid1 == 0:
    time.sleep(3)
    os.write(fde, b'hola gente')


pid2 = os.fork()

if pid2 == 0:
    while True:
        data = os.read(fdl, 11)
        print(data)
        