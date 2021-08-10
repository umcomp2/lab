# COMPUTACION II


## RECUPERATORIO TP2

Fecha de entrega: 24/08/2021


### Problema

Es necesario procesar imágenes con python, sin utilizar bibliotecas de procesamiento de imágenes. Para ello realizar una aplicación que abra y lea un archivo de imagen con formato portátil pixmap (ppm) indicado por la opcion "-f archivo"

El proceso debe lanzar 3 hilos para procesar la imagen. Debe ir leyendo la imagen por bloques de n bytes indicadas por la opcion "-n valor", y generar una nueva imagen igual a la anterior, pero espejada horizontalmente.

Cada hilo se debe encargar de procesar un color, rojo, verde o azul, segun corresponda y rehubicar los pixels en el lugar que le corresponda en la nueva imagen.



### Requerimientos

* La aplicación debe contener como mínimo 3 funciones.
* Debe procesar las opciones con getopt (agregar una opcion de ayuda) o con argparse.
* Debe usar el modulo Threading o Concurrent.futures.
* Debe manejar los errores.


#### Ejemplo modo de uso

~~~~~~~~~~~~~~~~~~~
$ ./rtp2.py -h
usage: rtp2.py [-h] -s SIZE -f FILE

Rtp2 - procesa ppm

optional arguments:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  Bloque de lectura
  -f FILE, --file FILE  archivo a procesar


$ ./rtp2.py -s 1024 -f tux.ppm 

Se espejo correctamente la imagen

$ ls *ppm
dog.ppm
dog_mirror.ppm

~~~~~~~~~~~~~~~~~~~


### Objetivos

* Manejo de archivos (apertura, escritura y cierre).
* Creación de hilos.
* Uso de mecanismos de sincronización.

### Referencias
man ppm
http://netpbm.sourceforge.net/doc/ppm.html

### Bonus Track
El programa debe pedir un argumento mas --blackwhite para además de espejar la imagen, dejarla en blanco y negro
