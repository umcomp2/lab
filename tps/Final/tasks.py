import cv2
from PIL import Image, ImageChops, ImageEnhance, ImageOps, ImageDraw, ImageFont
from celery import Celery
import json, codecs
import base64
from io import BytesIO
import numpy as np

app = Celery('tasks', broker='redis://localhost', backend='redis://localhost:6379')

@app.task
def abrir_imagen(image):
    imagen = Image.open(image)
    return imagen

@app.task
def escala_grises(image):
    imagen = abrir_imagen(image)
    imagen_gris = ImageOps.grayscale(imagen)
    buffered = BytesIO()
    imagen_gris.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    # imagen_gris.show()
    # imagen_gris.save("gris_"+ image)
    return img_str

@app.task
def invertir_colores(image):
    imagen = abrir_imagen(image)
    colores_inv = ImageChops.invert(imagen)
    buffered = BytesIO()
    colores_inv.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str

@app.task
def resaltar_luces(image, nro):
    imagen = abrir_imagen(image)
    #Entre mas grande es el enhance mas resalta las luces
    luces = ImageEnhance.Brightness(imagen).enhance(nro)
    buffered = BytesIO()
    luces.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str

@app.task
def contraste(image, nro):
    imagen = abrir_imagen(image)
    #Entre mas grande es el enhance mas contraste hace
    contraste = ImageEnhance.Contrast(imagen).enhance(nro)
    buffered = BytesIO()
    contraste.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str

@app.task
def espejado(image):
    imagen = abrir_imagen(image)
    espejada = ImageOps.mirror(imagen)
    buffered = BytesIO()
    espejada.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str

@app.task
def nitidez(image, nro):
    imagen = abrir_imagen(image)
    img_nit = ImageEnhance.Sharpness(imagen).enhance(nro)
    buffered = BytesIO()
    img_nit.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str

@app.task
def rotar_90(image):
    imagen = abrir_imagen(image)
    rotadaA90 = imagen.transpose(Image.ROTATE_90)
    buffered = BytesIO()
    rotadaA90.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str

@app.task
def rotar_270(image):
    imagen = abrir_imagen(image)
    rotadaA270 = imagen.transpose(Image.ROTATE_270)
    buffered = BytesIO()
    rotadaA270.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str

@app.task
def rotar_180(image):
    imagen = abrir_imagen(image)
    rotadaA180 = imagen.transpose(Image.ROTATE_180)
    buffered = BytesIO()
    rotadaA180.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str

@app.task
def tamaño(image, ancho, alto):
    imagen = abrir_imagen(image)
    ajuste = imagen.resize((ancho,alto))
    buffered = BytesIO()
    ajuste.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str

@app.task
def recortar(image, izq, sup, der, inf):
    imagen = abrir_imagen(image)
    recorte = imagen.crop((izq,sup,der,inf))
    buffered = BytesIO()
    recorte.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str

@app.task
def imagen_borrosa(image):
    img = cv2.imread(image)
    #La altura y el ancho (tupla) del kernel deben ser un numero positivo e impar
    img_borrosa = cv2.GaussianBlur(img, (11,11), 0)
    # cv2.imshow("borrosa_" + image, img_borrosa)
    # Preciona Esc o alguna tecla para que cierre
    retval, buffer= cv2.imencode(".jpg", img_borrosa)
    jpg_as_text = base64.b64encode(buffer)
    return jpg_as_text

@app.task
def enfocar(image):
    img = cv2.imread(image)
    resultado = cv2.fastNlMeansDenoisingColored(img, None, 15, 10, 7, 21)
    retval, buffer= cv2.imencode(".jpg", resultado)
    jpg_as_text = base64.b64encode(buffer)
    return jpg_as_text

@app.task
def texto(image, texto):
    imagen = abrir_imagen(image)
    draw = ImageDraw.Draw(imagen)
    font = ImageFont.truetype("DejaVuSerif.ttf", 60)
    #(ancho, alto) --> en el alto entre mas chico es mas arriba va
    #              --> en el ancho entre mas grande es mas a la derecha va
    draw.text((30,10), texto, font=font, fill="white")
    buffered = BytesIO()
    imagen.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str