El programa ejecuta la función chain n veces de manera asíncrona (n se puede setear mediante argumentos de consola, por defecto es 3).
La función chain a su vez llama a 2 funciones, primera y segunda. Estas dos funciones están creadas con 'async' lo que las hace corutinas que se
pueden ejecutar de manera asíncrona.
Chain llama a primera y segunda utilizando 'await', esto hace que la función chain se suspenda hasta que la corutina haya terminado.
Las funciones primera y segunda se suspenden llamando a la función async.sleep().
El resultado del código es que todas las funciones chain (que se ejecutan asíncronamente) se bloquean durante una duración de tiempo aleatoria, así todas terminan en tiempos diferentes en un orden distinto al que fueron llamadas.
Al terminar la ejecución de cada chain, se imprime en pantalla cuanto tiempo tardo cada una.

