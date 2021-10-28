Sockets + stdin [tcp_udp]

Escriba un programa cliente-servidor con sockets que tenga el siguiente comportamiento.

El usuario ejecutará el programa servidor pasándole tres argumentos:
-p: El puerto en el que va a atender el servicio (por defecto debe atender en todas las direcciones de red configuradas en el sistema operativo).
-t: Permitirá especificar el protocolo de transporte a utilizar. Las opciones válidas serán tcp o udp.
-f: Una ruta a un archivo de texto en blanco.
El servidor creará el socket con los datos especificados, y creará, si no existe, el archivo de texto.
El cliente recibirá tres argumentos por línea de comandos:
-a: La dirección IP del servidor
-p: El puerto en el que atiende el servidor
-t: El protocolo de transporte a usar. Por supuesto, para establecer la conexión correctamente ambos, cliente y servidor, deberán especificar el mismo protocolo de transporte.
El cliente comenzará a leer desde STDIN texto hasta que el usuario presione Ctrl+d.
El cliente enviará todo el contenido por el socket al servidor.
El servidor leerá todo el contenido desde el socket hasta que encuentre un EOF.
El servidor almacenará todo el contenido en el archivo de texto creado.
NOTA: los parámetros serán pasados por argumento y parseados usando getopt o argparse.

Ejemplo de carga del servidor:

python3 servidor.py -p 1234 -t tcp -f /tmp/archivo.txt
Ejemplo de carga del cliente:

python3 cliente.py -a 192.168.0.23 -p 1234 -t tcp