from common import *


matrix=[[['R','G','B'] for x in range(column)] for y in range(row)]

def llenar_matriz_rojo(rq):
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            sem.acquire()
            if rq.empty():
                sem.release()
                break
            byte = rq.get()
            matrix[y][x][0] = byte
            sem.release()

def llenar_matriz_verde(gq):
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            sem.acquire()
            if gq.empty():
                sem.release()
                break
            byte = gq.get()
            matrix[y][x][1] = byte
            sem.release()

def llenar_matriz_azul(bq):
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            sem.acquire()
            if bq.empty():
                sem.release()
                break
            byte = bq.get()
            matrix[y][x][2] = byte
            sem.release()

def invertirMatriz():
    for y in matrix:
        y.reverse()
    return matrix