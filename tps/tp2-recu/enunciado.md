# COMPUTACION II


## TP2

Fecha de entrega: 15/06/2021


### Problema

Es necesario procesar imágenes con python, sin utilizar bibliotecas de procesamiento de imágenes. Para ello realizar una aplicación que abra y lea un archivo de imagen con formato portátil pixmap (ppm) indicado por la opcion "-f archivo"

El proceso debe lanzar 3 hilos para procesar la imagen. Debe ir leyendo la imagen por bloques de n bytes indicadas por la opcion "-n valor", y generar una nueva imagen igual a la anterior, pero rotada 90 grados a la izquierda.

Cada hilo se debe encargar de procesar un color, rojo, verde o azul, segun corresponda y rehubicar los pixels en el lugar que le corresponda en la nueva imagen.



### Requerimientos

* La aplicación debe contener como mínimo 3 funciones.
* Debe procesar las opciones con getopt (agregar una opcion de ayuda) o con argparse.
* Debe usar el modulo Threading o Concurrent.futures.
* Debe manejar los errores.


#### Ejemplo modo de uso

~~~~~~~~~~~~~~~~~~~
$ ./tp2.py -h
usage: tp2..py [-h] -s SIZE -f FILE

Tp2 - procesa ppm

optional arguments:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  Bloque de lectura
  -f FILE, --file FILE  archivo a procesar


$ ./tp2.py -s 1024 -f tux.ppm 

Se rotó correctamente la imagen

$ ls *ppm
tux.ppm
tux_left.ppm

~~~~~~~~~~~~~~~~~~~


### Objetivos

* Manejo de archivos (apertura, escritura y cierre).
* Creación de hilos.
* Uso de mecanismos de sincronización.

### Referencias
man ppm
http://netpbm.sourceforge.net/doc/ppm.html

### Bonus Track
El programa debe pedir un argumento mas --sentido para rotar 90 grados a la izquierda o a la derecha

