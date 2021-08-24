import concurrent.futures
import time


def worker (seg):
    print("Voy a esperar....", seg)
    time.sleep(seg)
    print("espere....")
    return seg

segs = [1,2]
fut = []
#Creo pull de hijos
pul = concurrent.futures.ProcessPoolExecutor(2)
for i in segs:
    fut.append(pul.submit(worker,i))

#Ejecuto una función con uno de los hijos
for r in fut:
    print(r.result())  #Muestro el valor del retorno que tiene esa ejecucion a futuro de la tarea que va ajeceutar un hijo del pul que cree


