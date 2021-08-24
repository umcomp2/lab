import concurrent.futures
import time


def worker (seg):
    print("Voy a esperar....", seg)
    time.sleep(seg)
    print("espere....")
    return seg

segs = [1,2]

#Creo pull de hijos
pul = concurrent.futures.ProcessPoolExecutor(2)
r = pul.map(worker,segs)

#Ejecuto una función con uno de los hijos
for i in r:
    print(i) 