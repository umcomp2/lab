Práctica - Sockets INET/STREAM [remote_shell]

Escriba un programa cliente/servidor en python que permita ejecutar comandos GNU/Linux en una computadora remota.

Técnicamente, se deberá ejecutar un código servidor en un equipo “administrado”, y programar un cliente (administrador) que permita conectarse al servidor mediante sockets STREAM.

El cliente deberá darle al usuario un prompt en el que pueda ejecutar comandos de la shell.

Esos comandos serán enviados al servidor, el servidor los ejecutará, y retornará al cliente:

la salida estándar resultante de la ejecución del comando
la salida de error resultante de la ejecución del comando.
El cliente mostrará en su consola local el resultado de ejecución del comando remoto, ya sea que se haya realizado correctamente o no, anteponiendo un OK o un ERROR según corresponda.

Ejemplo de ejecución del cliente (la salida de los comandos corresponden a la ejecución en el equipo remoto.

diego@cryptos$ python3 ejecutor_cliente.py
> pwd
OK
/home/diego
> ls -l /home
OK
drwxr-xr-x 158 diego diego 20480 May 26 18:57 diego
drwx------   2 root  root  16384 May 28  2014 lost+found
drwxr-xr-x   6 andy  andy   4096 Jun  4  2015 user
> ls /cualquiera
ERROR
ls: cannot access '/cualquiera': No such file or directory
>
Agregue en el cliente la opción “-l <file>” para permitirle al usuario almacenar un log de toda la sesión (comandos ejecutados y su fecha/hora).