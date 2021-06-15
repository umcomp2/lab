import threading


def hilo(h):
    print(f'{h} Hilo ejecutando ..')
    return


if __name__ == '__main__':
    threads = ['Primer', 'Segundo']
    for i in threads:
        t = threading.Thread(target=hilo(i))
        t.start()
        t.join()

    # print('terminaron los hilos')
