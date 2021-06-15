import threading


lock = threading.Lock()


def depositar(monto, event):
    global saldo
    saldo += monto
    print(f'hilo1 depositando {monto} ......-> {saldo}')
    # event.set()


def extraer(monto, event):
    global saldo
    event_set = event.wait(1)
    if monto <= saldo:
        event.set()
    if event_set:
        saldo -= monto
        print(f'hilo2 extrayendo {monto} ......-> {saldo}')


if __name__ == '__main__':
    # lock = threading.Lock()
    evento = threading.Event()

    saldo = 100
    print(f'saldo = {saldo}')
    thread = list()

    for i in [depositar(1000, evento), extraer(500, evento)]:
        t = threading.Thread(target=i)
        thread.append(t)

    for i in thread:
        i.start()
        i.join()

    print(f'saldo = {saldo}')
