Tenemos dos funciones que devuelven un str, primera y segunda, en la cual le pasamos como parámetro desde el main un número n, que puede ser escrito por terminal o si no es un numero entre el 1 y el 3. En la funcion main iteramos esos numeros que mencionamos arriba para pasarselos como argumentos a la funcion chain la cual llama a la funcion primera en la que se duerme un tiempo determinado entre 1 y 10, para darle lugar a dos primeras más que tambien se ejecutan y se duermen. Una vez pasados esos segundos se van despertando acorde para ir retornando su número (n) como result{n}-A}.

Una vez que se ejecutó la funcion primera, en el chain se llama a la funcion segunda a la cual se le pasa como argumento el numero n,(que va del 1 al 3 o lo que se indicó en terminal), más los resultados de la funcion primera. La funcion segunda va realizando lo mismo que la primera pero ahora tambien con los resultados de la funcion primera que se le enviaron por argumento. 

Para finalizar la funcion chain nos devuelve el tiempo en el que se demoraron ambas funciones en retornar sus resultados.

