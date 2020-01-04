from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

PER_JURID_CHOICES = (
        ("FISICA", "FISICA"),
        ("JURIDICA", "JURIDICA")
        )


PROD_TIPO = (
        ("Bien", "Bien"),
        ("Servicio", "Servicio"),
        )

PROD_CATEGORIA = (
        ("Ventas", "Ventas"),
        ("Gastos", "Gastos"),
        ("Interno", "Interno")
        )

ORD_STATUS = (
        ("En Preparación", "En Preparación"),
        ("Confirmada", "Confirmada"),
        ("Cobrada", "Cobrada"),
        ("Cancelada", "Cancelada"),
        )

IVA = (
        (10.50, 10.50),
        (21.00, 21.00),
        )

class Cuenta(models.Model):
    "Modelo para Cuenta/Cliente"
    personeria = models.CharField(choices=PER_JURID_CHOICES, default="PJ", max_length=256)
    es_cliente = models.BooleanField(default=True)
    es_proveedor = models.BooleanField(default=False)
    nombre = models.CharField(max_length=256)
    calle = models.CharField(max_length=256)
    complemento = models.CharField(max_length=256)
    codigo_postal = models.CharField(max_length=256)
    ciudad = models.CharField(max_length=256)
    estado = models.CharField(max_length=256)
    pais = models.CharField(max_length=256)
    telefono = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    website = models.CharField(max_length=256)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('cuenta-details', args=[str(self.id)])

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    "Modelo para Producto"
    nombre = models.CharField(max_length=256)
    tipo = models.CharField(max_length=256, choices=PROD_TIPO, default="Bien")
    categoria = models.CharField(max_length=256, choices=PROD_CATEGORIA, default="Ventas")
    descripcion = models.CharField(max_length=256)
    precio_lista = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    precio_compra = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    stock = models.IntegerField(default=1, null=True)

    def get_absolute_url(self):
        return reverse('producto-details', args=[str(self.id)])

    def __str__(self):
        return self.nombre


class Orden(models.Model):
    "Modelo para orden"
    fecha_orden = models.DateTimeField(default=timezone.now)
    fecha_entrega = models.DateTimeField()
    orden_id = models.AutoField(primary_key=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, null=True, blank=True,
                              choices=ORD_STATUS, default='En Preparación')
    subtotal = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=20, null=True)

    def get_absolute_url(self):
        return reverse('orden-details', args=[str(self.orden_id)])

    def __unicode__(self):
        return self.orden_id


class OrdenProducto(models.Model):
    "Modelo para Order Line Items"
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio_lista = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    precio_especial = models.DecimalField(decimal_places=2, max_digits=20,
                                          null=True, blank=True)
    descuento = models.DecimalField(decimal_places=2, max_digits=20, null=True,
                                    blank=True)
    iva = models.DecimalField(decimal_places=2, max_digits=20, choices=IVA,
                              null=True, default=21.00)
    cantidad = models.IntegerField(default=1)
    subtotal = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=20, null=True)

    def get_absolute_url(self):
        return reverse('orden-details', args=[str(self.id)])

    def __unicode__(self):
        return self.orden_id
