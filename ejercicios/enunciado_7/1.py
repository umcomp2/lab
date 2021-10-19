import threading
import os
import time

def worker():
    pid = os.getpid()
    print("Ejecutando...")
    time.sleep(1.0)
    print("Soy un hilo del proceso {}".format(pid))

threads = []
for i in range(2):
    t = threading.Thread(target=worker())
    threads.append(t)
    t.start()
print("Terminaron los hilos")

for h in threads:
    h.join()
