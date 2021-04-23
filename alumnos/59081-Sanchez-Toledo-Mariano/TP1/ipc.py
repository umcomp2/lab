import os
import sys

fdl, fde = os.pipe()
proce1 = os.fork()

if proce1 == 0:
    print('Soy el hijo1\n')
    fd = os.open('tux.ppm',os.O_RDWR|os.O_CREAT)
    data = os.read(fd, 737280)
    os.write(fde, data)
    print(data)
    sys.exit(0)
    

proce2 = os.fork()

if proce2 == 0:
    print('Soy el proce hijo2\n', os.getpid())
    fx = os.open('tuxa.ppm', os.O_RDWR| os.O_CREAT)
    datanew = os.read(fdl, 737280)
    os.write(fx, datanew)

