from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CuentaForm, ProductoForm, OrdenForm
from .models import Cuenta, Producto, Orden, OrdenProducto, User
from django.views.generic import (CreateView, DeleteView, UpdateView,
                                  TemplateView, ListView, DetailView)
from .forms import (CuentaForm, ProductoForm, OrdenForm, OliForm, OliFormSet,
                    OliInlineFormSet)
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy
import json


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['ordenes'] = Orden.objects.all()
        context['cuentas'] = Cuenta.objects.all()
        return context


class CuentaCreate(LoginRequiredMixin, CreateView):
    form_class = CuentaForm
    model = Cuenta
    template_name = 'item-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cuenta'
        return context


class CuentaUpdate(LoginRequiredMixin, UpdateView):
    form_class = CuentaForm
    model = Cuenta
    template_name = 'item-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cuenta'
        return context


class CuentaDelete(LoginRequiredMixin, DeleteView):
    model = Cuenta
    template_name = 'confirm-delete.html'
    success_url = reverse_lazy('lista_cuentas')


class ListaCuentas(LoginRequiredMixin, ListView):
    model = Cuenta
    context_object_name = 'lista_cuentas'
    template_name = 'lista_cuentas.html'
    paginate_by = 10


class DetallesCuenta(LoginRequiredMixin, DetailView):
    model = Cuenta
    context_object_name = 'item'
    template_name = 'cuenta-details.html'

    def get_context_data(self, **kwargs):
        cuenta = self.object
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cuenta'
        context['lista_ordenes'] = Orden.objects.filter(cuenta = cuenta)
        return context


class ProductoCreate(LoginRequiredMixin, CreateView):
    form_class = ProductoForm
    model = Producto
    template_name = 'item-edit.html'
    context_object_name = 'Producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Producto'
        return context


class ProductoUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProductoForm
    model = Producto
    template_name = 'item-edit.html'
    context_object_name = 'Producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Producto'
        return context


class ProductoDelete(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'confirm-delete.html'
    success_url = reverse_lazy('lista_productos')


class DetallesProducto(LoginRequiredMixin, DetailView):
    model = Producto
    context_object_name = 'item'
    template_name = 'producto-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Producto'
        return context


class ListaProductos(LoginRequiredMixin, ListView):
    model = Producto
    context_object_name = 'lista_productos'
    template_name = 'lista_productos.html'
    paginate_by = 10

########### ORDENES ########################

class OrdenCreate(LoginRequiredMixin, CreateView):
    form_class = OrdenForm
    model = Orden
    template_name = 'item-edit.html'
    context_object_name = 'Orden'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Orden'
        precios = Producto.objects.all().values_list('nombre','precio_lista')
        context['precios'] = json.dumps(dict(precios), cls=DjangoJSONEncoder)
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form2 = OliInlineFormSet(
                queryset=OrdenProducto.objects.none()
                )
        return self.render_to_response(
            self.get_context_data(form=form, form2=form2))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form2 = OliInlineFormSet(
                request.POST,
                queryset=OrdenProducto.objects.none()
                )

        if form.is_valid() and form2.is_valid():
            orden = form.save(commit=False)
            orden.save()
            productos = form2.save(commit=False)
            for producto in productos:
                producto.orden = orden
                producto.save()
            return redirect('orden-details', pk=orden.pk)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2))


class OrdenUpdate(LoginRequiredMixin, UpdateView):
    model = Orden
    template_name = 'item-edit.html'
    context_object_name = 'Orden'
    fields = ['cuenta', 'vendedor', 'fecha_orden', 'fecha_entrega', 'subtotal',
            'total']

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        orden = Orden.objects.get(orden_id=pk)
        prods = OrdenProducto.objects.filter(orden=pk)
        form = OrdenForm(
            initial={'cuenta': orden.cuenta, 'vendedor': orden.vendedor,
                'fecha_orden': orden.fecha_orden, 'fecha_entrega':
                orden.fecha_entrega, 'status': orden.status,
                'subtotal': orden.subtotal, 'total': orden.total})
        form2 = OliInlineFormSet(queryset=prods)
        precios_list = Producto.objects.all().values_list('nombre','precio_lista')
        precios = json.dumps(dict(precios_list), cls=DjangoJSONEncoder)

        return render(request, self.template_name, {'form': form,
                                                    'form2': form2,
                                                    'precios':precios})

    def post(self, request, **kwargs):
        pk = self.kwargs['pk']
        orden = Orden.objects.get(orden_id=pk)
        prods = OrdenProducto.objects.filter(orden=pk)
        if request.method == 'POST':
            form = OrdenForm(request.POST, instance=orden)
            form2 = OliInlineFormSet(request.POST, queryset=prods)
            if form.is_valid() and form2.is_valid():
                orden = form.save(commit=False)
                orden.save()
                productos = form2.save(commit=False)
                for producto in form2.deleted_objects:
                    producto.delete()
                for producto in productos:
                    producto.orden = orden
                    producto.save()
            else:
                for producto in form2:
                    print(producto.errors)

        return redirect('orden-details', pk=pk)


class OrdenDelete(LoginRequiredMixin, DeleteView):
    model = Orden
    template_name = 'confirm-delete.html'
    success_url = reverse_lazy('lista_ordenes')


class DetallesOrden(LoginRequiredMixin, DetailView):
    model = Orden
    context_object_name = 'orden'
    template_name = 'orden-details.html'

    def get_context_data(self, **kwargs):
        orden = self.object
        context = super(DetallesOrden, self).get_context_data(**kwargs)
        context['titulo'] = 'Orden'
        context['olis'] = OrdenProducto.objects.filter(orden_id = orden)
        context['cliente'] = Cuenta.objects.filter(nombre = orden.cuenta)
        return context


class ListaOrdenes(LoginRequiredMixin, ListView):
    model = Orden
    context_object_name = 'lista_ordenes'
    template_name = 'lista_ordenes.html'
    paginate_by = 10


def confirmar_orden(request, pk):
    instance = Orden.objects.get(orden_id=pk)
    instance.status = "Confirmada"
    instance.save()
    return redirect('orden-details', pk=pk)


def cancelar_orden(request, pk):
    instance = Orden.objects.get(orden_id=pk)
    instance.status = "Cancelada"
    instance.save()
    return redirect('orden-details', pk=pk)


class PerfilUsuario(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'user-details.html'

    def get_context_data(self, **kwargs):
        username = self.object
        context = super(PerfilUsuario, self).get_context_data(**kwargs)
        context['ordenes'] = Orden.objects.filter(vendedor = username)
        context['cuentas'] = Cuenta.objects.filter(vendedor = username)
        return context

