from common import *


matrix=[[['R','G','B'] for x in range(column)] for y in range(row)]

def llenar_matriz_rojo(rq):
    try:
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                while rq.empty():
                    pass
                sem.acquire()
                print('red working')
                byte = rq.get()
                matrix[y][x][0] = byte
                sem.release()
    except:
        RuntimeError('Error en carga de color rojo, verifique que los valores ingresados sean correctos')
        

def llenar_matriz_verde(gq):
    try:
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                while gq.empty():
                    pass
                sem.acquire()
                print('green working')
                byte = gq.get()
                matrix[y][x][1] = byte
                sem.release()
    except:
        raise RuntimeError('Error en carga de color verde, verifique que los valores ingresados sean correctos')

def llenar_matriz_azul(bq):
    try:
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                while bq.empty():
                    pass
                sem.acquire()
                print('blue working')
                byte = bq.get()
                matrix[y][x][2] = byte
                sem.release()
    except:
        raise RuntimeError('Error en carga de color azul, verifique que los valores ingresados sean correctos')

def invertirMatriz():
    try:
        for y in matrix:
            y.reverse()
        return matrix
    except:
        raise RuntimeError('Error al realizar la matriz espejo, verifique que los valores ingresados sean correctos')