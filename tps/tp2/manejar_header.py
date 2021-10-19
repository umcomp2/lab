import os

def find_header(fd):
    leido = os.read(fd, 100)
    #leido = fd.read(100)
    ultima_linea = leido.find(b"255")
    header = leido[:ultima_linea + 4]
    size = len(header)
    return header, size

def uncomment(header):
    for i in range(header.count(b"\n# ")):
        comienzo_comentario = header.find(b"\n# ")
        sgte_enter = header.find(b"\n", comienzo_comentario + 1)
        header = header.replace(header[comienzo_comentario:sgte_enter], b"")
    return header

def rotate_header(old_header):
    first_enter = old_header.find(b"\n")
    first_line = old_header[:first_enter]
    second_enter = old_header.find(b"\n", first_enter + 1)
    second_line = old_header[first_enter + 1:second_enter]
    second_line_space = second_line.find(b" ")
    width = second_line[:second_line_space]
    height = second_line[second_line_space + 1:]
    third_line = old_header[second_enter + 1:]
    new_width = width
    new_height = height
    rotated_header = first_line + b"\n" + new_width + b" " + new_height + b"\n" + third_line
    rotated_header = rotated_header
    return rotated_header, int(new_width), int(new_height)
