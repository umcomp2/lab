import pymongo
from pymongo import MongoClient
from csv import *
import pprint
import json

class Pymongo():
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client["images"]
        self.collection1 = self.db["edits"]

    
    def see_inf(self):
        
        # Obtenemos la informacion de la coleccion ediciones
        info = self.collection1.find({"fecha":"23/2/2022"})
        pprint.pprint(info)

        # Obetenemos los nombres de las fotos editadas
        # keys = list(info.keys())
        # pprint.pprint(keys)

        # Obetenemos los valores de las fotos
        # values = list(info.values())



    def save_inf(self):
        pass

if __name__=="__main__":
    
    mongo = Pymongo()
    mongo.see_inf()
    exit(0)