PASOS A SEGUIR PARA USAR EL PROGRAMA: 
1- Clonar el repositorio --> https://github.com/militomba/lab.git 
2- Ingresar al directorio --> /lab/tps/final
3- Crear una base de datos Postgresql y completar en el archivo "postgres.py" los siguientes campos con el nombre de la base de datos, el usuario y contraseña correspondientes(los datos entre ' ' son ejemplos):
    dbname= 'pilatesdb2'
    user = 'milicomputacion'
    password = '1234'
    host = 'localhost' 
    port = '5432' #puerto predeterminado
4- Instalar Celery: pip install celery y Redis: sudo apt install redis-server, en caso de que no ya no los tengas instalado.
5- Ya una vez ubicado en el directorio mencionado en el punto 2, en 3 terminales diferentes, correr el servidor, el cliente y celery para poder ejecutar el programa:
    servidor: python3 server.py -i 192.168.54.175 -p 8010 (-i: ip, -p: puerto)
    cliente: (-u: tipo usuario)
        - administrador--> python3 client.py -i 192.168.54.175 -p 8010 -u admin
        - cliente --> python3 client.py -i 192.168.54.175 -p 8010 -u cliente
    celery: celery -A celeryApp worker --loglevel=INFO
La ip puede ser:
    -ipv4
    -ipv6

6- Una vez ejecutado el servidor, el cliente y el celery, en la terminal donde se ejecuto el cliente vamos a poder interactuar con las funciones correspondiente a cada tipo de usuario:
    USUARIO CLIENTE:
        -Sacar turno
        -Cancelar turno
    USUARIO ADMIN:
        -Agregar horario
        -Eliminar horario
        -Ver reservas 
