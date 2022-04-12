from pyexpat import model
from attr import field
from sympy import source
from yaml import serialize
from .models import Marca, Producto
from rest_framework import serializers


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Marca
        fields='__all__'


class ProductoSerializers(serializers.ModelSerializer):
    #para mostrar el nombre de la marcas en el listado de la descripcion del prducto en el JSON
    nombre_marca = serializers.CharField(read_only=True,source='marca.nombre')
    #otra forma de llamar al nombre de la marca apartir del serializer
    marca =MarcaSerializer(read_only=True)

    #para que salga un combox del listado de las marcas en el formulario de la API 
    marca_id = serializers.PrimaryKeyRelatedField(queryset=Marca.objects.all(),source = 'marca')
    nombre= serializers.CharField(required=True,min_length=3)

    def validate_nombre(self,value):
        existe= Producto.objects.filter(nombre__iexact=value).exists()

        if existe:
            raise serializers.ValidationError("Este producto ya existe")

        return value
   
    class Meta:
        model = Producto
        fields = '__all__'


