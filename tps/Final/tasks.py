import cv2
from PIL import Image, ImageChops, ImageEnhance, ImageOps, ImageDraw, ImageFont
from celery import Celery
import base64
from io import BytesIO
import pickle

app = Celery('tasks', broker='redis://localhost',
             backend='redis://localhost:6379')


@app.task
def abrir_imagen(image):
    imagen = Image.open(image)
    return imagen


@app.task
def funcion_generica(lista_datos):
    func = eval(lista_datos[1])
    resultado = func(lista_datos)
    return resultado

@app.task
def escala_grises(lista_datos):
    imagen = abrir_imagen(lista_datos[0])
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
def invertir_colores(lista_datos):
    imagen = abrir_imagen(lista_datos[0])
    colores_inv = ImageChops.invert(imagen)
    buffered = BytesIO()
    colores_inv.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str


@app.task
def resaltar_luces(lista_datos):
    imagen = abrir_imagen(lista_datos[0])
    # Entre mas grande es el enhance mas resalta las luces
    luces = ImageEnhance.Brightness(imagen).enhance(lista_datos[2])
    buffered = BytesIO()
    luces.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str


@app.task
def contraste(lista_datos):
    imagen = abrir_imagen(lista_datos[0])
    # Entre mas grande es el enhance mas contraste hace
    contraste = ImageEnhance.Contrast(imagen).enhance(lista_datos[2])
    buffered = BytesIO()
    contraste.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str


@app.task
def espejado(lista_datos):
    imagen = abrir_imagen(lista_datos[0])
    espejada = ImageOps.mirror(imagen)
    buffered = BytesIO()
    espejada.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str


@app.task
def nitidez(lista_datos):
    imagen = abrir_imagen(lista_datos[0])
    img_nit = ImageEnhance.Sharpness(imagen).enhance(lista_datos[2])
    buffered = BytesIO()
    img_nit.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str


@app.task
def rotar_90(lista_datos):
    imagen = abrir_imagen(lista_datos[0])
    rotadaA90 = imagen.transpose(Image.ROTATE_90)
    buffered = BytesIO()
    rotadaA90.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str


@app.task
def rotar_270(lista_datos):
    imagen = abrir_imagen(lista_datos[0])
    rotadaA270 = imagen.transpose(Image.ROTATE_270)
    buffered = BytesIO()
    rotadaA270.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str


@app.task
def rotar_180(lista_datos):
    imagen = abrir_imagen(lista_datos[0])
    rotadaA180 = imagen.transpose(Image.ROTATE_180)
    buffered = BytesIO()
    rotadaA180.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str


@app.task
def tamaño(lista_datos):
    imagen = abrir_imagen(lista_datos[0])
    ajuste = imagen.resize((lista_datos[2], lista_datos[3]))
    buffered = BytesIO()
    ajuste.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str


@app.task
def recortar(lista_datos):
    imagen = abrir_imagen(lista_datos[0])
    recorte = imagen.crop(
        (lista_datos[2], lista_datos[3], lista_datos[4], lista_datos[5]))
    buffered = BytesIO()
    recorte.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str


@app.task
def imagen_borrosa(lista_datos):
    img = cv2.imread(lista_datos[0])
    # La altura y el ancho (tupla) del kernel deben ser un numero positivo e impar
    img_borrosa = cv2.GaussianBlur(img, (11, 11), 0)
    # cv2.imshow("borrosa_" + image, img_borrosa)
    # Preciona Esc o alguna tecla para que cierre
    retval, buffer = cv2.imencode(".jpg", img_borrosa)
    jpg_as_text = base64.b64encode(buffer)
    img = str(jpg_as_text, "utf-8")
    return img


@app.task
def enfocar(lista_datos):
    img = cv2.imread(lista_datos[0])
    resultado = cv2.fastNlMeansDenoisingColored(img, None, 15, 10, 7, 21)
    retval, buffer = cv2.imencode(".jpg", resultado)
    jpg_as_text = base64.b64encode(buffer)
    img = str(jpg_as_text, "utf-8")
    return img


@app.task
def texto(lista_datos):
    imagen = abrir_imagen(lista_datos[0])
    draw = ImageDraw.Draw(imagen)
    font = ImageFont.truetype("DejaVuSerif.ttf", 60)
    # (ancho, alto) --> en el alto entre mas chico es mas arriba va
    #              --> en el ancho entre mas grande es mas a la derecha va
    draw.text((30, 10), lista_datos[2], font=font, fill="white")
    buffered = BytesIO()
    imagen.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str

# if __name__=="__main__":
#     a = imagen_borrosa("auto.jpg")
#     print(a)
