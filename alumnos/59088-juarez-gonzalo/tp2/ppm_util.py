import sys
import getopt

EOF = b""

def PPM_ALIGN(num, b_per_px):
    return num // b_per_px * b_per_px if num >= b_per_px else b_per_px

# @b_arr:   bytearray
def btoi(b_arr):
    ret = 0
    for i in range(len(b_arr)):
        ret = ret * 10 + (b_arr[i] - ord('0'))
    return ret

# @argv:    lista de argumentos
def parse_args(argv):
    opt, args = getopt.getopt(argv, "s:f:", ["size=", "file="])
    fname = ""
    rwsize = 0
    rot = 1

    for o in opt:
        oname = o[0].replace("-","")

        if oname == "sentido":
            rot = -1
            continue

        if oname[0] == "s":
            rwsize = int(o[1])
            continue

        if oname[0] == "f":
            fname = o[1]
            continue

        usagendie()

    if not fname or not rwsize:
        raise ValueError("Faltan parametros")

    # super mega validacion de formato de archivo
    if ".ppm" != fname[-4:]:
        raise ValueError("Archivo no tiene extensión ppm")

    return fname, rwsize

def usagendie():
    h = "usage: %s [-h] (-s|--size) SIZE (-f|--file) FILE\n\n" % __file__
    h += "TP1 - procesa ppm\n\n"
    h += "\t-h, --help\tMuestra esta ayuda\n"
    h += "\t-s, --size\tTamaño del bloque de lectura\n"
    h += "\t-f, --file\tArchivo a procesar\n"
    sys.stdout.write(h)
    sys.exit(0)
