#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os

os.write(1,b"hola\n")
os.read(0,4)


#notas:
# debe llevar la linea: #!/usr/bin/python3
#  para correr esto lo le debo dar permisos de ejecucion al archivo con el comand: chmod +x ejercitacion.py
#luego inicializo python3 como: ipython3
#para inciar el script utilizo: run ./ejercitacion.py