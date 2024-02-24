## FINAL

La idea en este proyecto es realizar un sistema de venta de tickets multicliente en el cual los clientes deberán establecer una conexión TCP con el servidor, por medio de serversocket, pasando por línea de comandos host y puerto mediante argparse, para así recibir información de los eventos disponibles por dicho canal y socilitar más információn sobre el evento que desee. Los datos se almacenarán en una base de datos Postgresql.

El servidor recibirá las operaciones desde el cliente y utilizará la cola de tareas distribuidas de redis y los workers celery para consumirlas. Cada tarea se encargará de realizar operaciones de entrada y salida a la base de datos para responder a las correspondientes peticiones.

Al establecer la conexión TCP se deberá pasar por argumento que tipo de usuario es, si es un "administrador" tendrá acceso a las tareas correspondientes para agregar un evento, mientras que si es un usuario "común" solo podrá consultar los eventos con sus respectivos sectores y sus entradas disponibles para luego hacer la compra correspondiente.

