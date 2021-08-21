
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
"""
print("hola mundo " + str(os.getpid()))
os.fork()
print("esto esta despues del fork "+ str(os.getpid()))
os.fork()
print("segundo fork "+ str(os.getpid()))

#hay una incosistencia de la cantidad de prints que hace(a veces 6 otras 7)
"""
for i in range(2):
    print (f'\n**********{i}***********')
    pid = os.fork()
    if pid == 0:
        print("\nWe are in the child process.")
        print (f"{os.getpid()}(child) just was created by {os.getppid()}.")
        pass
    else:
        print("\nWe are in the parent process.")
        print (f"{os.getpid()} (parent) just created {pid}")

#getppid() trae el id del proceso padre
#getpid() trae el id del proceso hijo