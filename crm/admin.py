from django.contrib import admin
from crm.models import Cuenta, Producto, Orden, OrdenProducto

admin.site.register(Cuenta)
admin.site.register(Producto)
admin.site.register(Orden)
admin.site.register(OrdenProducto)
