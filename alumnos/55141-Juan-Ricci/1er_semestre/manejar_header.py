import os

def quitar_header(leido):
    # quito los comentarios
    for i in range(leido.count(b"\n# ")):
        comienzo_comentario = leido.find(b"\n# ") # busca la posicion del primer \n# 
        sgte_enter = leido.find(b"\n", comienzo_comentario + 1) # busca la posicion del primer \n que le sigue al encontrado anteriormente
        leido = leido.replace(leido[comienzo_comentario:sgte_enter], b"") # reemplaza por un byte vacio todo lo que este entre la posicion del comienzo del comentario y la del \n que le sigue

    # encontrar encabezado
    primer_enter = leido.find(b"\n") # busca la posicion del primer \n
    primera_linea = leido[:primer_enter]
    segundo_enter = leido.find(b"\n", primer_enter + 1) # busca la posicion del \n que le sigue al anterior
    segunda_linea = leido[primer_enter + 1:segundo_enter]
    ultimo_enter = leido.find(b"\n", segundo_enter + 1) # busca la posicion del siguiente \n que sera el ultimo del encabezado
    tercera_linea = leido[segundo_enter + 1:ultimo_enter]
    header = leido[:ultimo_enter]
    #encabezado = leido[:ultimo_enter].decode()  # guarda todo lo que esta antes del ultimo enter

    # guardo el cuerpo
    cuerpo = leido[ultimo_enter + 1:] # guarda todo lo que esta despues del ultimo enter
    return cuerpo, primera_linea, segunda_linea, tercera_linea, header

def ppm_size(w_and_h):
    space = w_and_h.find(b" ")
    width = w_and_h[:space]
    height = w_and_h[space + 1:]
    return int(width), int(height)

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
    new_width = height
    new_height = width
    rotated_header = first_line + b"\n" + new_width + b" " + new_height + b"\n" + third_line
    rotated_header = rotated_header
    return rotated_header, int(new_width), int(new_height)
