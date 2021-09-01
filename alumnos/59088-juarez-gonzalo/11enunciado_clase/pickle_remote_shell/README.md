# REMOTE_SHELL SV & CLI

Servidor:
* Setear socket para servidor TCP
* Crear un pool de threads (de tamaño fijo)
* Usar la Queue de la libereria
de python, que ya se encarga de la sincronización
(creo que usa un mutex y una variable condicional
por los mensajes de error que he visto...)
* Un thread se queda escuchando por nuevas conexiones
y las coloca en la queue
* el pool de threads saca conexiones de la queue y
las trata en shell_loop()

Razonamiento: Es simple, con la Queue que ofrece python aun mas simple
y para los fines sirve bastante bien

Nota: Decidí aislar la conversión de string a byte y viceversa
en las funciones para recibir y enviar mensajes para aislar
un poco el resto del codigo de esos detalles.

# Smashing the pickling for fun and profit

Uso de oogabooga.py:
* ver codigo en oogabooga.py y acomodar hosts y ports segun corresponda
* nc -l [PORT] segun el puerto en donde se quiera controlar la maquina target
* correr sv.py si es que no esta corriendo ya
* correr oogabooga.py
* shell :)

Fuentes:
  - https://sensepost.com/cms/resources/conferences/2011/sour_pickles/B
  - https://checkoway.net/musings/pickle/
  - https://www.acunetix.com/blog/web-security-zone/what-is-reverse-shell/
