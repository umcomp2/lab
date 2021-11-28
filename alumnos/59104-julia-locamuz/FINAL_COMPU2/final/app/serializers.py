from rest_framework import serializers
from .models import *

# Serializers define the API representation.
class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'direccion', 'celular']

class CompraSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Compra
        fields = ['fecha', 'cliente']

class EstablecimientoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Establecimiento
        fields = ['nombre', 'direccion']

class ShowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Show
        fields = ['fecha', 'artista', 'precio_entrada', 'establecimiento']


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ['compra', 'show', 'cantidad']