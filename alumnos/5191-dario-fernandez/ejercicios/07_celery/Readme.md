Celery Remote Calc [celery_remote_calc]
Arquitectura
Crear un aplicación de calculadora cliente-servidor basándose en la siguiente infraestructura:

El cliente deberá establecer una conexión TCP contra el servidor, y por medio de dicho canal enviar al servidor las operaciones y operadores a calcular.

El servidor recibirá las operaciones desde el cliente, y utilizará la cola de tareas Redis y los workers Celery para ejecutarlas. Deberá esperar el resultado calculado por Celery, y luego enviar al cliente el resultado.

Diseñe el protocolo de comunicación cliente-servidor como lo crea conveniente.

Parámetros
Los parámetros recibidos por el cliente serán los siguientes:

-h ip_server
-p port
-o "operacion" (suma, resta, mult, div, pot)
-n ## (primer operando)
-m ## (segundo operando)
Los parámetros recibidos por el servidor serán:

-h ip_donde_atender
-p port
Ejemplo de ejecución:
Servidor:

python3 servidor_calc.py -h 0.0.0.0 -p 1234

Cliente:

python3 cliente_calc.py -h 127.0.0.1 -p 1234 -o suma -n 2 -m 3

> 5

Notas:
Puede ejecutar toda la infraestructura en la misma computadora, por ejemplo, corriendo:
Una terminal para el cliente
Una terminal para el servidor
Otra terminal con la cola de mensajes Redis
Otra terminal con los workers Celery