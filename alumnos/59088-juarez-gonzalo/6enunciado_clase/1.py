#!/usr/bin/env python3
import os
import sys
import getopt

RSIZE = 512
INFONL = 3  # total de lineas del header que aportan info en .ppm

if __name__ == "__main__":
    opt, args = getopt.getopt(sys.argv[1:], "f:")
    if len(opt) < 1 or len(opt[0]) < 1:
        raise ValueError("Faltan parametros")

    fname = opt[0][1]
    if not os.path.isfile(fname):
        raise FileNotFoundError("%s no es un archivo" % fname)

    # super mega validacion de formato de archivo
    if ".ppm" != fname[-4:]:
        raise ValueError("Archivo no tiene extensión ppm")

    fd = os.open(fname, os.O_RDONLY)

    rb = os.read(fd, RSIZE)

    nls = 0     # contador de '\n' en lineas que aportan info
    f_idx = 0   # indice posterior al ultimo newline de linea que aporta info
    cmmnt = 0   # flag que indica si prox '\n' corresponde a linea de comentario
    c = b""

    for i in range(RSIZE):
        if rb[i] == ord('#'):
            cmmnt |= 1
            continue
        if rb[i] == ord('\n') and cmmnt:
            cmmnt &= 0
            continue
        if rb[i] == ord('\n'):
            nls += 1
        if nls == INFONL:
            f_idx = i + 1
            break

    if nls != INFONL:
        raise ValueError("Demasiados comentarios en el header, header superior a %d bytes" % RSIZE)

    sys.stdout.write(rb[:f_idx].decode("utf8"))
    print("largo encabezado: %d" % (f_idx))
    os.close(fd)
