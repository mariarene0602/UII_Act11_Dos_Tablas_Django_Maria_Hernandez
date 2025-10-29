from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Perro
from .forms import ClienteForm, PerroForm
from django.db.models import Count

# Vistas para Clientes
def listar_clientes(request):
    clientes = Cliente.objects.annotate(num_perros=Count('perros')).order_by('apellido', 'nombre')
    return render(request, 'app_cliente/listar_clientes.html', {'clientes': clientes})

def detalle_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    perros_cliente = cliente.perros.all() # Accede a los perros relacionados
    return render(request, 'app_cliente/detalle_cliente.html', {'cliente': cliente, 'perros_cliente': perros_cliente})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'app_cliente/formulario_cliente.html', {'form': form, 'titulo': 'Crear Cliente'})

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('detalle_cliente', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'app_cliente/formulario_cliente.html', {'form': form, 'titulo': f'Editar Cliente: {cliente.nombre} {cliente.apellido}'})

def borrar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'app_cliente/confirmar_borrar_cliente.html', {'cliente': cliente})


# Vistas para Perros
def listar_perros(request):
    perros = Perro.objects.all().order_by('nombre')
    return render(request, 'app_cliente/listar_perros.html', {'perros': perros})

def detalle_perro(request, pk):
    perro = get_object_or_404(Perro, pk=pk)
    return render(request, 'app_cliente/detalle_perro.html', {'perro': perro})

def crear_perro(request):
    if request.method == 'POST':
        form = PerroForm(request.POST, request.FILES) # request.FILES para la imagen
        if form.is_valid():
            form.save()
            return redirect('listar_perros')
    else:
        form = PerroForm()
    return render(request, 'app_cliente/formulario_perro.html', {'form': form, 'titulo': 'Registrar Nuevo Perro'})

def editar_perro(request, pk):
    perro = get_object_or_404(Perro, pk=pk)
    if request.method == 'POST':
        form = PerroForm(request.POST, request.FILES, instance=perro) # request.FILES para la imagen
        if form.is_valid():
            form.save()
            return redirect('detalle_perro', pk=perro.pk)
    else:
        form = PerroForm(instance=perro)
    return render(request, 'app_cliente/formulario_perro.html', {'form': form, 'titulo': f'Editar Perro: {perro.nombre}'})

def borrar_perro(request, pk):
    perro = get_object_or_404(Perro, pk=pk)
    if request.method == 'POST':
        perro.delete()
        return redirect('listar_perros')
    return render(request, 'app_cliente/confirmar_borrar_perro.html', {'perro': perro})