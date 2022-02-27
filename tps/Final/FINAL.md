--------------------------->Arquitectura del aplicacion<--------------------------

+-----------+             +----------+                +-------+               +--------+
|  Cliente  | <---------> | Servidor | <------------> | Redis | <-----------> | Celery |
+-----------+             +----------+                +-------+               +--------+
                                |
                                |
                                |
                                |
                            +---------+
                            | Mongodb |
                            +---------+
Descripcion del programa:

El cliente se comunica con el servidor enviandole el nombre de una imagen, la edicion la cual le quiere aplicar a la imagen (la funcion), esas serian las dos cosas mas importantes que tendria que enviar el cliente. Luego tenemos otros parametros que se aplican a funciones como la nitidez (a la cual se le pasa un numero para saber la intesidad de la nitidez), el recortar la imagen le tenemos que pasar 4 parametros que son la parte izquierda, la parte superior, la parte dereche y la inferior para saber el recorte que se le va a hacer a la imagen, luego hay otras pero son muy parecidas.

El servidor va a recibir estos parametros, en forma de lista y segun la tarea que recibe es la tarea que encola al redis. Luego el Celery la consume la tarea del redis y una vez que se ejecuta la tarea, se devuelve el resultado al redis y luego la obtiene el servido para enviarsela al cliente.

Por ultimo el cliente, recibe la informacion del la transforma a imagen y la muestra.
