from tkinter import Widget
from attr import field, fields
from django import forms
from jsonschema import ValidationError
from .models import Contacto,Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validator import MaxSizeValidator
class ContactoForm(forms.ModelForm):
    #nombre= forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model = Contacto
        #fields=["nombre","correo","tipo_consulta","mensaje","aviso"]
        #declarar todos
        fields= '__all__'
        widgets ={
            "fecha_fabricacion":forms.SelectDateWidget()
        }
        

class ProductoForm(forms.ModelForm):

    nombre=forms.CharField(min_length=3,max_length=50)
    precio=forms.IntegerField(min_value=1)
    #validacion de la imagen ,puede ser nula
    imagen= forms.ImageField(required=False, validators=[MaxSizeValidator(max_file_size=2)])

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        #__iexact para q no se ceoten el la repeticon de nombre incluso may o min
        existe = Producto.objects.filter(nombre__iexact=nombre).exists()

        if existe:
            raise forms.ValidationError("Este nombre ya existe")
        
        return nombre

    class Meta:
        model= Producto
        fields = '__all__'

        widgets ={
            "fecha_fabricacion":forms.SelectDateWidget()
        }

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model =User
        fields=["username","first_name","last_name","email","password1","password2"]