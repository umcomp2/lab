## FINAL

La idea en este proyecto es realizar un sistema de venta de tickets multicliente en el cual los clientes deberán establecer una conexión TCP con el servidor para recibir información de las entradas disponibles por dicho canal, para luego enviar al servidor las operaciones y consultas en base a los tickets.
El servidor recibirá las operaciones desde el cliente y utilizará la cola de tareas redis y los workers celery, cada tarea se encargará de realizar operaciones de entrada y salida a la base de datos para responder a las correspondientes peticiones.
