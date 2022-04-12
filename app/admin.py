from multiprocessing.spawn import import_main_path
from re import search
from django.contrib import admin
from .models import Contacto, Marca,Producto
from .forms import ProductoForm
# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display =["nombre","precio","nuevo","marca"]
    list_editable=["precio"] #para editar el campo en el admin
    search_fields=["nombre"] #para buscar por nombre
    list_filter =["marca","nuevo"] #para filtrar por marca o nuevo
    list_per_page= 1 #paginacion
    form = ProductoForm


admin.site.register(Marca)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Contacto)

