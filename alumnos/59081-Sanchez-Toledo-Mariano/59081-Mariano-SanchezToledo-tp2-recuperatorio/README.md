El codigo funciona pero tiene problemas de optimización.

En el modulo common se encuentran variables que he utilizado en varios modulos.
El modulo Input se encarga de el input de la imagen, separar el header y body, y conseguir los datos de columna y fila de la imagen.
En el modulo Matriz se encuentran todas la funciones referidas al manejo de la matriz para generar un cuerpo nuevo para la imagen.
El modulo parse se encarga de manejar la libreria argparse.
En el modulo queue esta la funcion para el manejo de queues.
El modulo __main__ se encarga de instanciar lo necesario y correr el programa.

El problema de optimizacion existe en la comunicacion entre hilos y el algoritmo que carga las queues y el que procesa las queues, mientras mas pequeño es el bloque de lectura, mas lenta es dicha lectura. Recomiendo para probar el funcionamiento utilizar un bloque de 200000 bytes (va a leer todo el body), y para testear el funcionamiento de la comunicacion de hilos utilziar un bloque de 3 bytes. Estoy buscando formas de optimizar el codigo para que esto no sea necesario.

Modo de uso:

            python3 __main__.py -f FILE -s SIZE