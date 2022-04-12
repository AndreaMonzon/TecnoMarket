from tkinter import N
from django.urls import path,include

from app.models import Producto
from .views import ProductoViewset, home,contacto,galeria,agregar_producto,lista_productos,modificar_producto,eliminar_producto,registro,MarcaViewset
from rest_framework import routers

router=routers.DefaultRouter()
router.register('producto',ProductoViewset)
router.register('marca',MarcaViewset)



urlpatterns = [
    path('',home,name='home'),
    path('contacto/',contacto,name='contacto'),
    path('galeria/',galeria,name='galeria'),
    path('agregar-producto/',agregar_producto,name="agregar_producto"),
    path('listar-productos/',lista_productos,name="listar_productos"),
    path('modificar-productos/<id>/',modificar_producto,name="modificar_productos"),
    path('eliminar-producto/<id>/',eliminar_producto,name="eliminar_producto"),
    path('registro/',registro,name='registro'),
    path('api/',include(router.urls)),


]