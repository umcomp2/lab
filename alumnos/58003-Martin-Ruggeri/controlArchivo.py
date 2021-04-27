import os


fd = os.open("copia.py", os.O_RDWR | os.O_CREAT)
leido = os.read(fd, 15)
os.write(1, leido)

fd = os.open("archivo.txt", os.O_RDWR | os.O_CREAT)
print(fd)
os.write(fd, b"hola mundo\n")
fd = os.open("archivo.txt", os.O_RDWR)
print(fd)
leido = os.read(fd, 11)
os.write(1, leido)
os.close(1)
