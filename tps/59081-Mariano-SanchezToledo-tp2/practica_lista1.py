import random
pixeles=[]
body=[]
#lista = [[4, 0, 3], [5, 5, 4], [6, 6, 1], [9, 5, 4]]
for i in range(4):
    pixel = [random.randint(0,10),random.randint(0,10),random.randint(0,10)]
    pixeles.append(pixel)

for i in range(len(pixeles)):
    body.append([])
    body[i].append(pixeles[i])

def invertir(matriz):
    rotada =[]
    for i in range(len(matriz[0])):
        rotada.append([])
        for j in range(len(matriz)):
            rotada[i].append(matriz[len(matriz)-1-j][i])
    return rotada

if __name__ == '__main__':
    #print(pixeles)
    print(body)
    print(invertir(body))
