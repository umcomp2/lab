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

Desde el cli se puede tirar el servidor :). por ejemplo:
`kill -n 9 $(pgrep sv.py)` (aunque eso no sirve en el container porque busybox no tiene esas opciones para los comandos)
