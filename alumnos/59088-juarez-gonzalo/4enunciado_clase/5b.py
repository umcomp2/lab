#!/usr/bin/env python3
import os

# los prefijos R- y W- de los namedpipes corresponden
# al programa 5a.py, no es una confusión
RFIFO = "rfifo5a"
WFIFO = "wfifo5a"
RWSIZE = 256

if __name__ == "__main__":
    try:
        rfd = wfd = -1
        if not os.path.exists(RFIFO):
            os.mkfifo(RFIFO, 0o664)
        if not os.path.exists(WFIFO):
            os.mkfifo(WFIFO, 0o664)

        # primero RFIFO después WFIFO
        # el programa del otro lado del FIFO
        # debe abrir primero RFIFO y después WFIFO
        # si lo hace al reves -> deadlock (man 3 mkfifo)
        wfd = os.open(RFIFO, os.O_WRONLY)
        rfd = os.open(WFIFO, os.O_RDONLY)

        while (rdata := os.read(rfd, RWSIZE)) != b"":
            os.write(wfd, rdata.upper())
    finally:
        # aca con cerrar fd está bien, el otro programa se encarga
        # del unlink. Aunque podría agregarse un check en ambos
        # y unlink si fifo sigue existiendo (el otro programa no lo elimina antes)
        if wfd != -1:
            os.close(wfd)
        if rfd != -1:
            os.close(rfd)
