import pymongo
from pymongo import MongoClient
import csv
import base64
from io import BytesIO
from PIL import Image

client = MongoClient('mongodb://localhost:27017/')
db = client["images"]
collection = db["edits"]
    
def seeI_saveI():
    
    # Obtenemos la informacion de la coleccion ediciones
    info = collection.find()

    with open("mongodbInf.csv", "w+", newline = "") as csvfile:
        headers = ["_id", "edicion","imagen_edit","fecha","nombre"]
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for doc in info:
            writer.writerow(doc)

    # Query
    # info1 = collection.find_one({"nombre":"Nahuel"})
    # datos = info1["imagen_edit"]
    # img = base64.b64decode(datos)
    # img = BytesIO(img)
    # img = Image.open(img)
    # img.show()


if __name__=="__main__":
    
    seeI_saveI()