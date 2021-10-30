# Interpretacion codigo "chained.py"

El codigo comienza importando 3 modulos (*asyncio, random y time*) que seran utilizados posteriormente, luego define 4 funciones asincronas llamadas **"primera", "segunda", "chain" y "main"**. Posteriormente se procede a instanciar el metodo **main**.

## *Metodo main*

Dentro del metodo main se importa el paquete **sys** y despues se llama a al metodo **random.seed()** el cual se utiliza para inicializar un generador de numeros aleatorios. Se genera un array de 3 argumentos si no se le ha pasado ningun parametro. Se guarda el tiempo de inicio en la variable **start**. A partir de esto se llama a la corrutina *main* pasandole los argumentos generados anteriormente.

* ### *Corrutina main - alto nivel*
    Encargada de crear un loop de eventos los cuales retornan tres tareas de la corrutina **chain**.

* #### *Corrutina chain*
        Las tres tareas generadas ven a calcular un tiempo de ejecucion con las variables *start* y *end* y cada una ejecutara de forma asincrona las funciones definidas anteriormente *primera* y *segunda*.

* ##### *Corrutina primera*
            Esta funcion es llamada con el argumento *n* el cual representa el numero de la tarea. Al iniciar la funcion se genera un numero aleatorio entre 0 y 10 dado por *random.randint(0,10)* que este luego sera utilizado para dormir la funcion con *await asyncio.sleep()* de manera asincrona mostrando los valores por pantalla. A medida que cada tarea vaya despertando el loop de eventos las volvera a llamar mostrando el resultado.

        Una vez finalizada la ejecucion de la funcion *primera* se vuelve a la funcion *chain* la cual llamara a la funcion *segunda* pasando como argumentos el numero de tarea y el resultado de obtenido en *primera*

* ##### *Corrutina segunda*
            Esta funcion tiene un comportamiento similar a *primera* con diferencia de que muestra el resultado obtenido en **primera** y luego la ejecucion retornara el resultado obtenido de manera encadenada. Finalmente volvera a la funcion *chain*.

        Finalizando la corrutina *chain* se calculara el tiempo de ejecucion de cada tarea y se mostrara el resultado obtenido de las dos corrutinas (**primera y segunda**).

Por ultimo el metodo main calculara el tiempo de ejecucion de todo el programa y lo mostrara en pantalla.

