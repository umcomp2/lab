
leido = open('dog.ppm', 'rb').read()

for i in range(leido.count(b"\n# ")):
    comienzo_comentario = leido.find(b"\n# ") # busca el primer byte \n# 
    byte_sgte_al_com = leido.find(b"\n", comienzo_comentario + 1) # busca el primer \n a partir del siguiente byte del que comienza el comentario
    leido = leido.replace(leido[comienzo_comentario:byte_sgte_al_com], b"") # reemplaza desde donde comienza el comentario hasta donde comienza el siguiente /n por vacio

        # sacar encabezado
primer_n = leido.find(b"\n") + 1
seg_n = leido.find(b"\n", primer_n) + 1
ultima_barra_n = leido.find(b"\n", seg_n) + 1
encabezado = leido[:ultima_barra_n].decode() # esto es lo que esta antes de la ultima barra'''

        # guardo el cuerpo
cuerpo = leido[ultima_barra_n:] # esto es lo q esta despues de la ultima barra