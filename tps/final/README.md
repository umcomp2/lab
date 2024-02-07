## FINAL

La idea en este proyecto es realizar un sistema de venta de tickets multicliente en el cual los clientes deberán establecer una conexión TCP pasando por la línea de comandos host y puerto para la conexión con el servidor y así recibir información de las entradas disponibles por dicho canal, para luego enviar al servidor las operaciones y consultas en base a los tickets.
El servidor recibirá las operaciones desde el cliente y utilizará la cola de tareas redis y los workers celery, cada tarea se encargará de realizar operaciones de entrada y salida a la base de datos para responder a las correspondientes peticiones.

Al establecer la conexión TCP se deberá pasar por argumento que tipo de usuario es, si es un "administrador" tendrá acceso al celery para poder agregar eventos. Mientras que si es un usuario "común" solo podrá ver los eventos y consultar por ellos para ver los sectores y entradas disponibles.
