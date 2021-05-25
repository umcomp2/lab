
leido = open('dog.ppm', 'rb').read()

for i in range(leido.count(b"\n# ")):
    comienzo_comentario = leido.find(b"\n# ") # busca el primer byte \n# 
    byte_sgte_al_com = leido.find(b"\n", comienzo_comentario + 1) # busca el primer \n a partir del siguiente byte del que comienza el comentario
    leido = leido.replace(leido[comienzo_comentario:byte_sgte_al_com], b"") # reemplaza desde donde comienza el comentario hasta donde comienza el siguiente /n por vacio
        # sacar encabezado
primer_n = leido.find(b"\n") #+ 1
print(primer_n)
seg_n = leido.find(b"\n", primer_n + 1) #+ 1
print(seg_n)
ultima_barra_n = leido.find(b"\n", seg_n + 1)# + 1
print(ultima_barra_n)
encabezado = leido[:ultima_barra_n].decode() # esto es lo que esta antes de la ultima barra'''
print(encabezado)
        # guardo el cuerpo
cuerpo = leido[ultima_barra_n:] # esto es lo q esta despues de la ultima barra


# CODIGO EXTRA USADO AL IR HACIENDO EL RECUPERATORIO DEL TP1

'''
#import os
#import matplotlib.pyplot as plt
#from itertools import islice
'''

# Divdir lo leido de a 3 bytes
'''listado = list(islice(chunk, 3)) # divide el chunk cada 3 bytes
rojo.append(listado[0]) # agrego el primer item de la lista a la lista rojo
verde.append(listado[1]) # agrego el segundo item de la lista a la lista verde
azul.append(listado[2]) # agrego el tercer item de la lista a la lista azul'''

# Al dividir lo leido de a 3 bytes tenia que ir guardando c/u en una nueva lista. Lo mismo debia hacer con el verde y el azul
'''lista_rojo = list()
for i in rojo: 
        lista_rojo.append(i) # cada valor del color rojo lo guardo en una sola lista
lista_rojo.sort() # ordeno la lista
f_rojo = Counter(lista_rojo) # relizo un conteo de cada item y lo guardo pero me lo vuelve a desordenar (se guarda como tuplas)
rojo_ordenado = sorted(f_rojo.items()) # ordeno la lista que me devolvio la funcion Counter    
for tupla in rojo_ordenado:
        lista = list(tupla) # las tuplas son inmutables por lo que debo convertir c/u en una lista,
        #lista[1] = lista[1] * escala_rojo # cambiar el valor necesitado
        tupla = tuple(lista) # y volverla a convertir en tupla
        filtro_rojo.write(str(tupla) + '\n') # escribo el resultado en el archivo que cree anteriormente'''

# Funcion para crear histograma
'''def crear_hist(pipe, filename, chunk_sz, color, rojo, verde, azul):
    h_r, h_v, h_a = read_and_dump(pipe, filename, chunk_sz, color, rojo, verde, azul)
    plt.hist(h_r, bins=256, color = 'red', edgecolor='red')
    plt.savefig('red.png')
    plt.cla()
    plt.hist(h_v, bins=256, color = 'green', edgecolor='green')
    plt.savefig('green.png')
    plt.cla()
    plt.hist(h_a, bins=256, color = 'blue', edgecolor='blue')
    plt.savefig('blue.png')
    plt.cla()'''

