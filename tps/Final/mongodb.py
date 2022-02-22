import pymongo
from pymongo import MongoClient
from csv import *

class Pymongo():
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client["images"]
        self.collection1 = self.db["edits"]
        self.collection2 = self.db["clients"]

    
    def see_inf(self):
        
        # Obtenemos la informacion de la coleccion ediciones
        info = self.collection1.find()

        # Obtenemos la informacion de la coleccion clientes
        info = self.collection1.find()

        # Obetenemos la informacion de la primera columna de cada fila
        # keys = list(info.keys())

        # Obetenemos la informacion de la segunda columna de cada fila
        # values = list(info.values())



    def save_inf(self):
        pass