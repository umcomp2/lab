import random



def invertir(matriz):
    rotada =[]
    for i in range(len(matriz[0])):
        rotada.append([])
        for j in range(len(matriz)):
            rotada[i].append(matriz[len(matriz)-1-j][i])
    return rotada

if __name__ == '__main__':
    rint = random.randint
    lista = []
    tag = 0
    while tag != 4:
        lista += [[[rint(0,10), rint(0,10), rint(0,10)]]]
        tag += 1


    rotada = invertir(lista)
    print(lista)
    print(rotada)