from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('registro/', views.registro, name='registro'),
    path('cuenta/login/', views.login_cliente, name='login_cliente'),
    path('cuenta/logout/', views.logout_cliente, name='logout_cliente'),
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/quitar/<int:producto_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('carrito/confirmar/', views.confirmar_compra, name='confirmar_compra'),
    path('login/', views.login_admin, name='login_admin'),
    path('logout-admin/', views.logout_admin, name='logout_admin'),
    path('panel-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('panel-admin/producto/nuevo/', views.product_form, name='producto_nuevo'),
    path('panel-admin/producto/<int:pk>/editar/', views.product_form, name='producto_editar'),
    path('panel-admin/producto/<int:pk>/archivar/', views.toggle_archivo, name='producto_archivar'),
    path('panel-admin/producto/<int:pk>/eliminar/', views.delete_producto, name='producto_eliminar'),
    path('panel-admin/usuario/<int:pk>/editar/', views.user_form, name='usuario_editar'),
    path('panel-admin/usuario/<int:pk>/toggle/', views.toggle_user, name='usuario_toggle'),
    path('panel-admin/usuario/<int:pk>/eliminar/', views.delete_user, name='usuario_eliminar'),
]
