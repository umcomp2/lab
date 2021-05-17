import threading
import time
def worker(num):
    print("{} hilo ejecutando".format(num))
args = ["Primer","Segundo"]
threads = []
for i in args:
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
    time.sleep(1.0)
print("Terminaron los hilos")
for h in threads:
    h.join()
