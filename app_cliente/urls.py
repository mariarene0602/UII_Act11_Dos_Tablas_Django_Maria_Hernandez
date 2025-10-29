# app_cliente/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URLs para Clientes
    path('', views.listar_clientes, name='listar_clientes'), # Página de inicio
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:pk>/', views.detalle_cliente, name='detalle_cliente'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:pk>/borrar/', views.borrar_cliente, name='borrar_cliente'),

    # URLs para Perros
    path('perros/', views.listar_perros, name='listar_perros'),
    path('perros/crear/', views.crear_perro, name='crear_perro'),
    path('perros/<int:pk>/', views.detalle_perro, name='detalle_perro'),
    path('perros/<int:pk>/editar/', views.editar_perro, name='editar_perro'),
    path('perros/<int:pk>/borrar/', views.borrar_perro, name='borrar_perro'),
]