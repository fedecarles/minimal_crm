from django.forms.models import modelformset_factory
from django import forms
from crm import models


class CuentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CuentaForm, self).__init__(*args, **kwargs)
        for field in self._meta.fields:
            attrs = {'class':'form-control'}
            if self.fields[field].widget.__class__.__name__ == "DateTimeInput":
                attrs.update({'type':'date'})
            if self.fields[field].widget.__class__.__name__ == "CheckboxInput":
                attrs.update({'type':'checkbox', 'class':''})
            self.fields[field].widget.attrs.update(attrs)

    class Meta:
        model = models.Cuenta
        fields = ['personeria', 'nombre', 'calle', 'complemento',
                  'codigo_postal', 'pais', 'estado', 'ciudad', 'telefono',
                  'email', 'website','vendedor', 'es_cliente', 'es_proveedor']


class ProductoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        for field in self._meta.fields:
            attrs = {'class':'form-control'}
            if self.fields[field].widget.__class__.__name__ == "DateTimeInput":
                attrs.update({'type':'date'})
            if self.fields[field].widget.__class__.__name__ == "CheckboxInput":
                attrs.update({'type':'checkbox', 'class':''})
            self.fields[field].widget.attrs.update(attrs)

    class Meta:
        model = models.Producto
        fields = ['tipo', 'categoria', 'nombre', 'descripcion',
                  'precio_lista', 'precio_compra', 'stock']


class OrdenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenForm, self).__init__(*args, **kwargs)
        for field in self._meta.fields:
            attrs = {'class':'form-control'}
            if self.fields[field].widget.__class__.__name__ == "DateTimeInput":
                attrs.update({'type':'date'})
            if self.fields[field].widget.__class__.__name__ == "CheckboxInput":
                attrs.update({'type':'checkbox', 'class':''})
            self.fields[field].widget.attrs.update(attrs)

    class Meta:
        model = models.Orden
        fields = ['fecha_orden', 'cuenta', 'vendedor', 'fecha_entrega',
                  'status', 'subtotal', 'total']


class OliForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OliForm, self).__init__(*args, **kwargs)
        for field in self._meta.fields:
            attrs = {'class':'form-control'}
            if self.fields[field].widget.__class__.__name__ == "DateTimeInput":
                attrs.update({'type':'date'})
            if self.fields[field].widget.__class__.__name__ == "CheckboxInput":
                attrs.update({'type':'checkbox', 'class':''})
            self.fields[field].widget.attrs.update(attrs)

    class Meta:
        model = models.OrdenProducto
        fields = ['producto', 'precio_lista', 'precio_especial', 'descuento',
                  'iva', 'cantidad', 'subtotal', 'total']


OliFormSet = forms.modelformset_factory(
        models.OrdenProducto,
        form=OliForm,
        extra=1,
        widgets={'producto': forms.TextInput(attrs={'class':'form-control'})},
        can_delete=True
        )


OliInlineFormSet = forms.inlineformset_factory(
        models.Orden,
        models. OrdenProducto,
        extra=1,
        fields=('producto', 'precio_lista', 'precio_especial', 'descuento',
                'iva', 'cantidad', 'subtotal', 'total'),
        formset=OliFormSet,
        min_num=1,
        widgets={'producto': forms.Select(attrs={'class':'form-control'}),
                 'precio_lista': forms.TextInput({'class':'form-control', 'readonly':'true'}),
                 'precio_especial': forms.TextInput(attrs={'class':'form-control'}),
                 'descuento': forms.TextInput(attrs={'class':'form-control'}),
                 'iva': forms.Select(attrs={'class':'form-control'}),
                 'cantidad': forms.TextInput(attrs={'class':'form-control'}),
                 'subtotal': forms.TextInput(attrs={'class':'form-control'}),
                 'total': forms.TextInput(attrs={'class':'form-control'}),
                 },
        can_delete=True,
        )

