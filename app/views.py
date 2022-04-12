from ast import Return
from django.http import Http404
from django.shortcuts import render ,redirect,get_object_or_404
from .models import Producto,Marca
from django.contrib import messages
# Create your views here.
from .forms import ContactoForm,ProductoForm,CustomUserCreationForm
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required,permission_required
from rest_framework import viewsets
from .serializers import ProductoSerializers,MarcaSerializer


class MarcaViewset(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

class ProductoViewset(viewsets.ModelViewSet):
    #Trae todos los productos
    queryset = Producto.objects.all()
    #aplicando el serializador que convierte a todos los productos en JSON
    serializer_class = ProductoSerializers

    #para filtar por nombre

    def get_queryset(self):
        productos = Producto.objects.all()

        nombre = self.request.GET.get('nombre')

        #pregunto si viene en la url la busqueda por el nombre del producto
        #__contains lista todos los productos que sean igual al nombre o contengan 
        if nombre:
            productos = productos.filter(nombre__contains=nombre)
        
        return productos


def home(request):
    productos=Producto.objects.all()
    data={
    'productos':productos
    }
    return render(request,'app/home.html',data)

def contacto(request):
    data ={
        'form':ContactoForm()
    }
    if request.method == 'POST':
        formulario =ContactoForm(data=request.POST)
        if formulario.is_valid():
          formulario.save()
          data["mensaje"] = "contacto guardado"
        else:
            data["form"]=formulario


    return render(request,'app/contacto.html',data)

def galeria(request):
    return render(request,'app/galeria.html')


# para agreagar producto se requiere permiso
@permission_required('app.add_producto')
def agregar_producto(request):
    data = {
        'form':ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Producto registrado ")
           
        else:
          data["form"]= formulario

    return render(request,'app/producto/agregar.html',data)


@permission_required('app.view_producto')

def lista_productos(request):
    productos=Producto.objects.all()
    page = request.GET.get('page',1)

    try:
      paginator = Paginator(productos,5)
      productos=paginator.page(page)
    except:
        raise Http404


    data ={
        'entity':productos,
        'paginator':paginator
    }
    return render (request,'app/producto/listar.html',data)

@permission_required('app.change_producto')

def modificar_producto(request,id):
    producto= get_object_or_404 (Producto,id=id)
    data={
        'form':ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST,instance=producto,files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Modificado correctamente ")
            return redirect(to="listar_productos")
        data["form"]=formulario

    return render(request, 'app/producto/modificar.html',data)
@permission_required('app.delete_producto')

def eliminar_producto(request,id):
    
    producto=Producto.objects.get(id=id)
    producto.delete()
    messages.success(request,'Producto eliminado')
    return redirect('listar_productos')


def registro(request):
    data = {
        'form':CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data['username'],password=formulario.cleaned_data['password1'])
            login(request,user)
            messages.success(request,'Te has registrado correctamente')
            return redirect(to='home')
    

    return render(request,'registration/registro.html',data)