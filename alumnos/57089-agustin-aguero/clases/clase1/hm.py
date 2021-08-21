
#a este archivo le dimos permisos chmod 0744 
#!/usr/bin/python3     //agrega un interprete python3 (va con el #)
# -*- coding: UTF-8 -*-       --> esto lo agregamos si usasemos python2 (va con el #)

print("hola mundo")    #printeamos esto a alto nivel

#mirar lo que es un "shebang"
        #era lo del path, el cual voy a usar el #!/usr/bin/python3



#si lo quisieramos hacer en bajo nivel:
from os import write
#write(fd,length)   -> str  esa es la sintaxis
write(1,b"hola?\n")     #el 1 es el monitor, si le pusiesemos un 0 estariamos con el teclado
                        # la b indica que no vamos a usar string, vamos a usar bites
                        #corremos este archivo con: python3 hm.py

#si quisieramos hacer una entrada de teclado

import os
        #read(fd,length) -> str      fd es file descriptor
leidos=os.read(0,10)        #el 0 es el teclado, esperara una entrada de 10 bites de longitud
print(leidos)


entrada= input()
