from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    ClienteLoginForm,
    ProductoForm,
    RegistroUsuarioForm,
)
from .models import Producto


def index(request):
    productos = Producto.objects.filter(archivado=False).order_by('-id')[:6]
    total_productos = Producto.objects.filter(archivado=False).count()
    carrito = request.session.get('carrito', {})
    total_carrito = sum(carrito.values())

    context = {
        'productos': productos,
        'total_productos': total_productos,
        'total_carrito': total_carrito,
    }
    return render(request, 'Ferreteria/index.html', context)


def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso. Ya puedes comprar en la tienda.')
            return redirect('inicio')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'Ferreteria/registro.html', {'form': form})


def login_cliente(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        form = ClienteLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}.')
            return redirect('inicio')
    else:
        form = ClienteLoginForm()

    return render(request, 'Ferreteria/login_cliente.html', {'form': form})


def logout_cliente(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('inicio')


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito = request.session.get('carrito', {})
    key = str(producto.pk)
    carrito[key] = carrito.get(key, 0) + 1
    request.session['carrito'] = carrito
    request.session.modified = True
    messages.success(request, f'{producto.nombre} fue agregado al carrito.')
    return redirect('inicio')


def quitar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    key = str(producto_id)

    if key in carrito:
        if carrito[key] <= 1:
            del carrito[key]
        else:
            carrito[key] -= 1

    request.session['carrito'] = carrito
    request.session.modified = True
    return redirect('carrito')


def carrito(request):
    carrito_data = request.session.get('carrito', {})
    items = []
    total = 0

    for producto_id, cantidad in carrito_data.items():
        producto = Producto.objects.filter(pk=producto_id, archivado=False).first()
        if not producto:
            continue

        subtotal = producto.precio * cantidad
        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })
        total += subtotal

    cantidad_total = sum(item['cantidad'] for item in items)
    context = {
        'items': items,
        'total': total,
        'cantidad_total': cantidad_total,
    }
    return render(request, 'Ferreteria/carrito.html', context)


@login_required(login_url='login_cliente')
def confirmar_compra(request):
    carrito_data = request.session.get('carrito', {})

    if not carrito_data:
        messages.warning(request, 'Tu carrito está vacío. Agrega productos antes de confirmar la compra.')
        return redirect('carrito')

    request.session['carrito'] = {}
    request.session.modified = True
    messages.success(request, 'Compra confirmada. Tu pedido queda pendiente de preparación y puedes seguir agregando productos.')
    return redirect('carrito')


def login_admin(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, 'Bienvenido al panel administrativo.')
            return redirect('admin_dashboard')

        messages.error(request, 'Credenciales inválidas o no tienes permisos de administrador.')

    return render(request, 'Ferreteria/login_admin.html')


@login_required(login_url='login_admin')
@staff_member_required(login_url='login_admin')
def admin_dashboard(request):
    productos = Producto.objects.order_by('-id')
    usuarios = User.objects.order_by('-date_joined')
    return render(request, 'Ferreteria/admin_dashboard.html', {
        'productos': productos,
        'usuarios': usuarios,
    })


@login_required(login_url='login_admin')
@staff_member_required(login_url='login_admin')
def product_form(request, pk=None):
    producto = Producto.objects.get(pk=pk) if pk else None
    form = ProductoForm(request.POST or None, instance=producto)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto guardado correctamente.')
        return redirect('admin_dashboard')

    return render(request, 'Ferreteria/product_form.html', {
        'form': form,
        'producto': producto,
    })


@login_required(login_url='login_admin')
@staff_member_required(login_url='login_admin')
@require_POST
def toggle_archivo(request, pk):
    producto = Producto.objects.get(pk=pk)
    producto.archivado = not producto.archivado
    producto.save()
    estado = 'archivado' if producto.archivado else 'visible'
    messages.success(request, f'El producto quedó {estado} en el feed de compradores.')
    return redirect('admin_dashboard')


@login_required(login_url='login_admin')
@staff_member_required(login_url='login_admin')
@require_POST
def delete_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    producto.delete()
    messages.success(request, 'Producto eliminado correctamente.')
    return redirect('admin_dashboard')


@login_required(login_url='login_admin')
@staff_member_required(login_url='login_admin')
@require_POST
def toggle_user(request, pk):
    usuario = User.objects.get(pk=pk)
    if request.user.pk == usuario.pk:
        messages.error(request, 'No puedes desactivar tu propia cuenta de administrador.')
        return redirect('admin_dashboard')

    usuario.is_active = not usuario.is_active
    usuario.save()
    estado = 'activado' if usuario.is_active else 'desactivado'
    messages.success(request, f'Usuario {usuario.username} {estado} correctamente.')
    return redirect('admin_dashboard')


@login_required(login_url='login_admin')
@staff_member_required(login_url='login_admin')
@require_POST
def delete_user(request, pk):
    usuario = User.objects.get(pk=pk)
    if request.user.pk == usuario.pk:
        messages.error(request, 'No puedes eliminar tu propia cuenta de administrador.')
        return redirect('admin_dashboard')

    usuario.delete()
    messages.success(request, 'Usuario eliminado correctamente.')
    return redirect('admin_dashboard')


@login_required(login_url='login_admin')
def logout_admin(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('login_admin')
