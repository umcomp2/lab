from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Cliente(models.Model):
    # si no aclaro primary key, me la genera sola. 
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    celular = models.CharField(max_length=12)
    
    def __str__(self):
        return self.nombre + ' ' + self.apellido

class Compra(models.Model):
    fecha = models.DateField()
    cliente = ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {} {}'.format(self.cliente.nombre, self.cliente.apellido, str(self.fecha)) 

class Establecimiento(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Show(models.Model):
    fecha = models.DateField(verbose_name=str)
    artista = models.CharField(max_length=100)
    precio_entrada = models.FloatField()
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE )

    def __str__(self):
        return self.artista + ' ' + self.establecimiento.nombre

class Item(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return 'compra {} show {}'.format(str(self.compra.id), self.show.artista)
