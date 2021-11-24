import threading


lock = threading.Lock()


def depositar(monto, c):
    global saldo
    with c:
        saldo += monto
        print(f'hilo1 depositando {monto} ......-> {saldo}')
        c.notifyAll()
    # return


def extraer(monto, c):
    global saldo
    with c:
        c.wait
        saldo -= monto
        print(f'hilo2 extrayendo {monto} ......-> {saldo}')


if __name__ == '__main__':
    cond = threading.Condition()

    saldo = 100
    print(f'saldo = {saldo}')
    thread = list()

    for i in [depositar(1000, cond), extraer(500, cond)]:
        t = threading.Thread(target=i)
        thread.append(t)

    for i in thread:
        i.start()
    # thread[0].join()

    print(f'saldo = {saldo}')
