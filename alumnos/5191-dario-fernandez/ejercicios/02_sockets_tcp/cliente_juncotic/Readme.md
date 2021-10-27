El código server_compu2.py (repo git de la cátedra) implementa un protocolo que corre sobre TCP y que tiene los siguientes comandos:

hello|<nombre>
email|<correo_electronico>
key|<clave_hardodeada>
exit

Estos comandos deben ser enviados al servidor en ese mismo orden, y por cada uno el servidor responderá con uno de los siguientes códigos:

200: OK
400: Comando válido, pero fuera de secuencia.
500: Comando inválido.
404: Clave errónea.
405: Cadena nula.
Al obtener un valor distinto de 200 el servidor seguirá esperando el valor correcto en el siguiente intento, por lo que no será necesario reiniciar la conexión.

Programe un cliente TCP que pueda conectar contra el servidor pidiéndole al usuario los datos uno por uno, y analizando las respuestas desde el servidor para notificar al cliente ante cualquier problema.

Ejemplo de ejecución:

python3 cliente_remoto.py -h URL -p 2222

La salida del servidor, en el caso de haber llevado a cabo todos los pasos correctamente, será algo similar a esto:

27-05-2020_19:39:16|diego|diego@yyy.com|Compu2_2020|('127.0.0.1', 47980)

