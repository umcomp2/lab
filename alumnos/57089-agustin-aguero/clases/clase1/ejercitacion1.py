
"""
1 - realize un programa que lea todos los datos ingresados desde stdin, 
   e invierta el orden de las letras en cada  palabra, enviandolo a stdout.

Ejemplo de funcionamiento

# echo -e  "hola mundo \n nos vemos" | ./invierte.py 

aloh odnum 
son somev
"""
#!/usr/bin/python3

import sys

while True:
   stdin_fileno = sys.stdin.readline()
   entrada = str(stdin_fileno)
   lista = list(entrada.split(" "))
   lista_b = []
   for x in lista:
      lista_b.append(x[::-1])
   linea = (' '.join(lista_b)).strip('')
   sys.stdout.write(linea )
     
     #el programa termina con: ctrl + z












 


