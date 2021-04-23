import os

fd = os.open('yacht.ppm',os.O_RDWR|os.O_CREAT)
fx = os.open('tuxa.ppm',os.O_RDWR|os.O_CREAT)

info = os.read(fd,1000000)
os.write(fx, bytes(info))
