Para poder usar el programa correctamente en primer lugar se debe clonar el siguiente repositorio: https://github.com/IvanCsir/lab. Luego se deberá ingresar al siguiente directorio: /lab/tps/final.

En segundo lugar, debemos crear una base de datos Postgresql y cambiar los siguientes campos según corresponda en el archivo postgresql_config.py
    -dbname = 'ticketsdb'
    -user = 'postgres'
    -password = 'admin'
    -host = 'localhost' 
    -port = '5432'

En tercer lugar, debemos instalar redis y celery, para ello haremos los siguientes comandos.
Redis:
    - sudo apt install redis-server
    - redis-cli

Celery:
    -pip3 install celery

Una vez instalado todo, ya en el directorio mencionado, ejecutar 3 pestañas en la consola.
En la primera ejecutaremos: celery -A celery_admin worker --loglevel=INFO, para ejecutar el celery.

En la segunda pestaña ejecutamos el servidor: python3 server.py -p 2701 -pr 4
La opción -pr (protocolo) si es 4 atenderá en ipv4, si es 6 en la interfaz de loopback de ipv6

Por último, en la pestaña restante ejecutamos el cliente y empezamos a interactuar:
python3 client.py -p 2701 -pr 4. Eñ protocolo dependerá de como se lanzó el servidor.

Añadir el argumento -r admin para poder agregar y eliminar eventos.


