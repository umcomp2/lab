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
    #encabezado = leido[:ultimo_enter].decode()  # guarda todo lo que esta antes del ultimo enter

    # guardo el cuerpo
    cuerpo = leido[ultimo_enter + 1:] # guarda todo lo que esta despues del ultimo enter
    return cuerpo, primera_linea, segunda_linea, tercera_linea

def ppm_size(w_and_h):
    space = w_and_h.find(b" ")
    width = w_and_h[:space]
    height = w_and_h[space + 1:]
    return int(width), int(height)