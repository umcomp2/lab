import cv2
from PIL import Image, ImageChops, ImageEnhance, ImageOps, ImageDraw, ImageFont

def abrir_imagen(image):
    imagen = Image.open(image)
    return imagen

def escala_grises(image):
    imagen = abrir_imagen(image)
    imagen_gris = ImageOps.grayscale(imagen)
    # imagen_gris.show()
    # imagen_gris.save("gris_"+ image)
    return imagen_gris

def invertir_colores(image):
    imagen = abrir_imagen(image)
    colores_inv = ImageChops.invert(imagen)
    # colores_inv.show()
    # colores_inv.save("coloresInv_"+ image)
    return colores_inv

def resaltar_luces(image, nro):
    imagen = abrir_imagen(image)
    #Entre mas grande es el enhance mas resalta las luces
    luces = ImageEnhance.Brightness(imagen).enhance(nro)
    # luces.show()
    return luces

def contraste(image, nro):
    imagen = abrir_imagen(image)
    #Entre mas grande es el enhance mas contraste hace
    contraste = ImageEnhance.Contrast(imagen).enhance(nro)
    # contraste.show()
    return contraste

def espejado(image):
    imagen = abrir_imagen(image)
    espejada = ImageOps.mirror(imagen)
    # espejada.show()
    return espejada

def nitidez(image, nro):
    imagen = abrir_imagen(image)
    img_nit = ImageEnhance.Sharpness(imagen).enhance(nro)
    # img_nit.show()
    return img_nit

def rotar_90(image):
    imagen = abrir_imagen(image)
    rotadaA90 = imagen.transpose(Image.ROTATE_90)
    # rotadaA90.show()
    return rotadaA90

def rotar_270(image):
    imagen = abrir_imagen(image)
    rotadaA270 = imagen.transpose(Image.ROTATE_270)
    # rotadaA270.show()
    return rotadaA270

def rotar_180(image):
    imagen = abrir_imagen(image)
    rotadaA180 = imagen.transpose(Image.ROTATE_180)
    # rotadaA180.show()
    return rotadaA180

def tamaño(image, ancho, alto):
    imagen = abrir_imagen(image)
    ajuste = imagen.resize((ancho,alto))
    # ajuste.show()
    return ajuste

def recortar(image, izq, sup, der, inf):
    imagen = abrir_imagen(image)
    recorte = imagen.crop((izq,sup,der,inf))
    # recorte.show()
    return recorte

def unir_imagenes(image1, image2):
    imagen1 = abrir_imagen(image1)
    imagen2 = abrir_imagen(image2)
    #Las imagenes tienen que tener el mismo tamaño
    if imagen1.size == imagen2.size:
        final = Image.new("RGB", (800,600), "black")
        final.paste(imagen1, (0,0))
        final.paste(imagen2, (400,0))
        # final.show()
    return final

def imagen_borrosa(image):
    img = cv2.imread(image)
    #La altura y el ancho (tupla) del kernel deben ser un numero positivo e impar
    img_borrosa = cv2.GaussianBlur(img, (11,11), 0)
    # cv2.imshow("borrosa_" + image, img_borrosa)
    # Preciona Esc o alguna tecla para que cierre
    # cv2.waitKeyEx(0)
    # cv2.imwrite("borroso_" + image , img_borrosa)
    return img_borrosa

def bordes(image):
    img = cv2.imread(image)
    edge_img = cv2.Canny(img, 100, 200)
    # cv2.imshow("bordes_" + image, edge_img)
    # cv2.waitKeyEx(0)
    return edge_img

def enfocar(image):
    img = cv2.imread(image)
    resultado = cv2.fastNlMeansDenoisingColored(img, None, 15, 10, 7, 21)
    # cv2.imshow("enfoque_" + image, resultado)
    # cv2.waitKey(0)
    return resultado

def texto(image, texto):
    imagen = abrir_imagen(image)
    draw = ImageDraw.Draw(imagen)
    font = ImageFont.truetype("DejaVuSerif.ttf", 60)
    #(ancho, alto) --> en el alto entre mas chico es mas arriba va
    #              --> en el ancho entre mas grande es mas a la derecha va
    draw.text((30,10), texto, font=font, fill="white")
    # imagen.show()
    return imagen