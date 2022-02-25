import pymongo
from pymongo import MongoClient
from csv import *
import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client["images"]
collection = db["edits"]
    
def see_inf():
    
    # Obtenemos la informacion de la coleccion ediciones
    info = collection.find()

    # Obetenemos los nombres de las fotos editadas
    for doc in info:
        pprint.pprint(doc.keys())

    # Obetenemos los valores de las fotos
    # values = list(info.values())



def save_inf(self):
    pass

if __name__=="__main__":
    
    see_inf()