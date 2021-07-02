def inicializar_matriz(width, height):
    matriz = [[[0,0,0] for i in range(width)]for i in range(height)]
    return matriz

def inicializar_matriz_espejada(width, height):
    matriz = [[[0,0,0] for i in range(height)]for i in range(width)]
    return matriz