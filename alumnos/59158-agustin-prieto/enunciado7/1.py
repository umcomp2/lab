import threading


def hilo():
    print('ejecutando ..')
    return


if __name__ == '__main__':

    for i in range(2):
        t = threading.Thread(target=hilo)
        t.start()
        t.join()
    print('terminaron los hilos')
