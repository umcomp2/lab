from PIL import Image

imagen = Image.open('dog.ppm')

rotada = imagen.transpose(Image.ROTATE_90)

rotada.save('rotated_dog.ppm')