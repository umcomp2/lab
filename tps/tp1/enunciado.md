# COMPUTACION II


## TP1

Fecha de entrega: 27/04/2021


### Problema

Es necesario procesar imágenes con python, sin utilizar bibliotecas de procesamiento de imágenes. Para ello realizar una aplicación que abra y lea un archivo de imagen con formato portátil pixmap (ppm) indicado por la opcion "-f archivo"

El proceso padre debe lanzar tres procesos hijos para procesar la imagen ( uno por cada color RGB ). Debe ir leyendo la imagen por bloques de n bytes indicadas por la opcion "-n valor", y alimentar el mecanismo de IPC que crea conveniente con ellos.

Cada proceso hijo debe procesar los datos que recibe del mecanismo de IPC y crear el histograma para color, rojo, verde o azul, segun corresponda y
grabarlos en tres archivos distintos.

Cuando el proceso padre termina de leer el archivo, debe cerrarlo, esperar que los hijos terminen de trabajar y mostrar un mensaje si fue exitoso.


### Requerimientos

* La aplicación debe contener como mínimo 3 funciones.
* Debe procesar las opciones con getopt (agregar una opcion de ayuda) o con argparse.
* Debe usar el modulo multiprocessing.
* Debe manejar los errores.


#### Ejemplo modo de uso

~~~~~~~~~~~~~~~~~~~
$ ./tp1.py -h
usage: tp1.py [-h] -s SIZE -f FILE

Tp1 - procesa ppm

optional arguments:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  Bloque de lectura
  -f FILE, --file FILE  archivo a procesar


$ ./tp1.py -s 1024 -f tux.ppm 

Se generaron correctamente los 3 histogramas

$ ls *ppm
tux.ppm
b_tux.txt
g_tux.txt
r_tux.txt

~~~~~~~~~~~~~~~~~~~


### Objetivos

* Manejo de archivos (apertura, escritura y cierre).
* Creación de procesos.
* Uso de mecanismos de IPC.

### Referencias
man ppm

man pgmhist

http://netpbm.sourceforge.net/doc/ppm.html

https://es.wikipedia.org/wiki/Histograma


### Bonus Track
Los procesos hijos adicionalmente deben generar un archivo tipo ppm con su filtro

