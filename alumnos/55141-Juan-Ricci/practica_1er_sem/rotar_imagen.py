import os
from array import array

def quitar_header(leido):
    # quito los comentarios
    for i in range(leido.count(b"\n# ")):
        comienzo_comentario = leido.find(b"\n# ") # busca la posicion del primer \n# 
        sgte_enter = leido.find(b"\n", comienzo_comentario + 1) # busca la posicion del primer \n que le sigue al encontrado anteriormente
        leido = leido.replace(leido[comienzo_comentario:sgte_enter], b"") # reemplaza por un byte vacio todo lo que este entre la posicion del comienzo del comentario y la del \n que le sigue

    # encontrar encabezado
    primer_enter = leido.find(b"\n") # busca la posicion del primer \n
    segundo_enter = leido.find(b"\n", primer_enter + 1) # busca la posicion del \n que le sigue al anterior
    segunda_linea = leido[primer_enter + 1:segundo_enter]
    ultimo_enter = leido.find(b"\n", segundo_enter + 1) # busca la posicion del siguiente \n que sera el ultimo del encabezado
    tercera_linea = leido[segundo_enter + 1:ultimo_enter]
    #encabezado = leido[:ultimo_enter].decode()  # guarda todo lo que esta antes del ultimo enter

    # guardo el cuerpo
    cuerpo = leido[ultimo_enter + 1:] # guarda todo lo que esta despues del ultimo enter
    fd.close()
    return cuerpo, segunda_linea, tercera_linea

def inicializar_matriz(height, width):
    matriz = [[[0,0,0] for i in range(width)]for i in range(height)]
    return matriz

def rotar_rojo(altura):
    global matriz
    global cuerpo
    global columna_r
    global fila_r
    for i in range(0,len(cuerpo)-1,3):
        matriz[fila_r][columna_r][0] = cuerpo[i]
        fila_r-=1
        if fila_r == -1:
            fila_r = altura -1 
            columna_r += 1

def rotar_verde(altura):
    global matriz
    global cuerpo
    global columna_g
    global fila_g
    for i in range(1,len(cuerpo),3):
        matriz[fila_g][columna_g][1] = cuerpo[i]
        fila_g-=1
        if fila_g == -1:
            fila_g = altura -1 
            columna_g += 1

def rotar_azul(altura):
    global matriz
    global cuerpo
    global columna_b
    global fila_b
    for i in range(2,len(cuerpo),3):
        matriz[fila_b][columna_b][2] = cuerpo[i]
        fila_b-=1
        if fila_b == -1:
            fila_b = altura -1 
            columna_b += 1

if __name__ == '__main__':

    fd = open('test.ppm', 'rb')

    leido = fd.read()
    cuerpo, hw , c = quitar_header(leido)

    espacio = hw.find(b" ")
    altura = hw[:espacio]
    ancho = hw[espacio + 1:]
    height = int(ancho)
    width = int(altura)
    c = int(c)

    fd.close()

    print(cuerpo)
    matriz = inicializar_matriz(height, width)
    print(matriz)

    fila_r = height - 1
    columna_r = 0
    fila_g = height -1
    columna_g = 0
    fila_b = height -1
    columna_b = 0

    rotar_rojo(height)
    rotar_verde(height)
    rotar_azul(height)
    print(matriz)

    imagen_rotada = open('test_rotado.ppm', 'w')
    header = f'P6\n{height} {width}\n255\n'
    imagen_rotada.write(header)
    imagen_rotada.close()
    imagen_rotada = open('test_rotado.ppm', 'a')

    for i in matriz:
        for j in i:
            for k in j:
                imagen_rotada.write(chr(k))

    fd.close()