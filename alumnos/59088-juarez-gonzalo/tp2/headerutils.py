NCOLORS = 3

def COLORSIZE(header):
    if header["maxcolor"] & 0xff00:
        return 2
    return 1

def BYTES_PER_PX(header):
    return COLORSIZE(header) * NCOLORS

def HEADERSIZE(header):
    return len(header["content"])

def BODYSIZE(header):
    return COLORSIZE(header) * BYTES_PER_PX(header) * header["rows"] * header["cols"]

def FILESIZE(header):
    return HEADERSIZE(header) + BODYSIZE(header)

def PPM_ALIGN(header, size):
    b_per_px = BYTES_PER_PX(header)
    if size < b_per_px:
        return b_per_px
    return size // b_per_px * b_per_px

# cálculos de offset en el cuerpo (para calcular en el archivo hay que sumar HEADERSIZE(header))

def BODYPX_OFFSET(header, offset):
    return offset // NCOLORS

def PXBYTE_OFFSET(header, offset):
    return offset % NCOLORS

def BODYBYTE_OFFSET(header, pixel, offset):
    return NCOLORS * pixel + PXBYTE_OFFSET(header, offset)

def PIXEL2RC(header, pixel):
    row = pixel // header["cols"]
    col = pixel % header["cols"]
    return row, col

def RC2PIXEL(header, row, col):
    return row * header["cols"] + col

def header_cp(header):
    return {**header}

RCLINE = 2
def _swap_rc(header):
    rows = header["rows"]
    cols = header["cols"]
    lines = header["content"].split(b"\n")
    count = RCLINE

    for i in range(len(lines)):
        if b"#" not in lines[i]:
            count -= 1
        if not count:
            lines[i] = bytes("%s %s" % (str(rows), str(cols)), "utf8")
            break
    header["content"] = b"\n".join(lines)

def swap_rc(header):
    _swap_rc(header)
    header["rows"], header["cols"] = header["cols"], header["rows"]
