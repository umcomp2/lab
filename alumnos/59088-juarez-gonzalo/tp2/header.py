from ppm_util import *

NCOLORS = 3                 # cantidad de colores
INFONL = 3                  # total de lineas del header que aportan info en .ppm

# =============== header ================
#
# header sin comentarios es de la forma:
#                MAGIC\nCOLS ROWS\nMAX_BYTE_VAL\n

# @hdr:  diccionario header
def h_calc_colorsize(hdr):
    maxval = hdr["maxcolor"]
    if maxval & 0xff00:
        return 2
    return 1

# @hdr:  diccionario header
def h_calc_totalbytes(hdr):
    return hdr["ops"]["calc_colorsize"](hdr) * hdr["b_per_px"] * hdr["cols"] * hdr["rows"]

# Parsea el header de un archivo .ppm, populando el diccionario hdr global con informacion
# @hdr:  diccionario header
# @rb:  Bytes donde se encuentra el header
def parse_header(hdr, rb):
    global INFONL
    global NCOLORS

    hdr_uncmmnt = bytearray()
    nls = 0         # contador de '\n' en lineas que aportan info
    f_idx = 0       # indice posterior al ultimo newline de linea que aporta info
    in_cmmnt = 0    # flag que indica si prox '\n' corresponde a linea de comentario
    c = b""

    for i in range(len(rb)):

        if rb[i] == ord('#'):
            in_cmmnt |= 1
            continue

        if rb[i] == ord('\n') and in_cmmnt:
            in_cmmnt &= 0
            continue

        if rb[i] == ord('\n'):
            nls += 1

        if not in_cmmnt:
            hdr_uncmmnt += rb[i].to_bytes(1, byteorder="big")

        if nls == INFONL:
            f_idx = i + 1
            break

    if nls != INFONL:
        raise ValueError("Demasiados comentarios en el header, header superior a %d bytes" % INIT_RSIZE)

    hdr_fields = hdr_uncmmnt.split(b'\n')
    hdr["content"] = rb[:f_idx]
    hdr["f_idx"] = f_idx
    hdr["magic"] = hdr_fields[0]

    hdr["cols"], hdr["rows"] = hdr_fields[1].split(b" ")
    hdr["cols"] = btoi(hdr["cols"])
    hdr["rows"] = btoi(hdr["rows"])
    hdr["maxcolor"] = btoi(hdr_fields[2])

    hdr["b_per_px"] = hdr["ops"]["calc_colorsize"](hdr) * NCOLORS

header_ops = {
    "calc_totalbytes": h_calc_totalbytes,
    "calc_colorsize": h_calc_colorsize,
    "parse": parse_header
}

header = {
    "content": "",
    "f_idx": "",

    "magic": "",
    "cols": 0,
    "rows": 0,

    "maxcolor": 0,
    "b_per_px": 0,

    "ops": header_ops,
}

def header_init():
    global header
    return {**header}

def header_cp(hdr):
    return {**hdr}
