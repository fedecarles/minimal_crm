"""simple_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from crm.views import (Index, CuentaCreate, CuentaDelete, CuentaUpdate, ProductoCreate,
                       ProductoUpdate, ProductoDelete, OrdenCreate, OrdenUpdate,
                       OrdenDelete, DetallesOrden, ListaOrdenes, DetallesCuenta,
                       ListaCuentas, DetallesProducto, ListaProductos,
                       confirmar_orden, cancelar_orden, PerfilUsuario)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('', Index.as_view(), name='index'),

    path('cuenta/add/', CuentaCreate.as_view(), name='cuenta-add'),
    path('cuenta/update/<int:pk>/', CuentaUpdate.as_view(), name='cuenta-update'),
    path('cuenta/<int:pk>/delete/', CuentaDelete.as_view(), name='cuenta-delete'),
    re_path(r'^cuenta/(?P<pk>\d+)$', DetallesCuenta.as_view(), name='cuenta-details'),
    path('lista_cuentas/', ListaCuentas.as_view(), name='lista_cuentas'),

    path('producto/add/', ProductoCreate.as_view(), name='producto-add'),
    path('producto/update/<int:pk>/', ProductoUpdate.as_view(), name='producto-update'),
    path('producto/<int:pk>/delete/', ProductoDelete.as_view(), name='producto-delete'),
    re_path(r'^producto/(?P<pk>\d+)$', DetallesProducto.as_view(), name='producto-details'),
    path('lista_productos/', ListaProductos.as_view(), name='lista_productos'),

    path('orden/add/', OrdenCreate.as_view(), name='orden-add'),
    path('orden/update/<int:pk>/', OrdenUpdate.as_view(), name='orden-update'),
    path('orden/<int:pk>/delete/', OrdenDelete.as_view(), name='orden-delete'),
    re_path(r'^orden/(?P<pk>\d+)$', DetallesOrden.as_view(), name='orden-details'),
    path('lista_ordenes/', ListaOrdenes.as_view(), name='lista_ordenes'),

    path('orden/confirmar/<int:pk>/', confirmar_orden, name='confirmar-orden'),
    path('orden/cancelar/<int:pk>/', cancelar_orden, name='cancelar-orden'),

    re_path(r'^usuario/(?P<pk>\d+)$', PerfilUsuario.as_view(), name='user-details'),
]
