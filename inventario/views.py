from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import MarcaLlanta, Llanta, Inventario, Entradas
from .forms import MarcaLlantaForm, LlantaForm, InventarioForm, EntradasForm


class MarcaListView(ListView):
	model = MarcaLlanta
	template_name = 'inventario/marca_list.html'
	paginate_by = 20

	def get_queryset(self):
		qs = super().get_queryset()
		q = self.request.GET.get('q')
		if q:
			return qs.filter(nombre__icontains=q)
		return qs


class LlantaListView(ListView):
	model = Llanta
	template_name = 'inventario/llanta_list.html'
	paginate_by = 20

	def get_queryset(self):
		qs = super().get_queryset().select_related('marca')
		q = self.request.GET.get('q')
		if q:
			return qs.filter(
				Q(marca__nombre__icontains=q) |
				Q(modelo__icontains=q) |
				Q(ancho__icontains=q) |
				Q(alto__icontains=q) |
				Q(rin__icontains=q)
			)
		return qs


class LlantaCreateView(LoginRequiredMixin, CreateView):
	model = Llanta
	form_class = LlantaForm
	template_name = 'inventario/llanta_form.html'
	success_url = reverse_lazy('inventario:llanta_list')


class LlantaUpdateView(LoginRequiredMixin, UpdateView):
	model = Llanta
	form_class = LlantaForm
	template_name = 'inventario/llanta_form.html'
	success_url = reverse_lazy('inventario:llanta_list')


class LlantaDeleteView(LoginRequiredMixin, DeleteView):
	model = Llanta
	template_name = 'inventario/llanta_confirm_delete.html'
	success_url = reverse_lazy('inventario:llanta_list')


class InventarioListView(ListView):
	model = Inventario
	template_name = 'inventario/inventario_list.html'
	paginate_by = 20

	def get_queryset(self):
		qs = super().get_queryset()
		q = self.request.GET.get('q')
		if q:
			return qs.filter(
				Q(descripcion__icontains=q) |
				Q(marca__icontains=q) |
				Q(producto_clave__icontains=q)
			)
		return qs


class InventarioCreateView(LoginRequiredMixin, CreateView):
	model = Inventario
	form_class = InventarioForm
	template_name = 'inventario/inventario_form.html'
	success_url = reverse_lazy('inventario:inventario_list')


class InventarioUpdateView(LoginRequiredMixin, UpdateView):
	model = Inventario
	form_class = InventarioForm
	template_name = 'inventario/inventario_form.html'
	success_url = reverse_lazy('inventario:inventario_list')


class InventarioDeleteView(LoginRequiredMixin, DeleteView):
	model = Inventario
	template_name = 'inventario/inventario_confirm_delete.html'
	success_url = reverse_lazy('inventario:inventario_list')


class EntradasListView(ListView):
	model = Entradas
	template_name = 'inventario/entradas_list.html'
	paginate_by = 20

	def get_queryset(self):
		qs = super().get_queryset().select_related('talleres', 'llantas')
		q = self.request.GET.get('q')
		if q:
			return qs.filter(
				Q(talleres__razon_social__icontains=q) |
				Q(producto_clave__icontains=q)
			)
		return qs


class EntradasCreateView(LoginRequiredMixin, CreateView):
	model = Entradas
	form_class = EntradasForm
	template_name = 'inventario/entradas_form.html'
	success_url = reverse_lazy('inventario:entradas_list')


class EntradasUpdateView(LoginRequiredMixin, UpdateView):
	model = Entradas
	form_class = EntradasForm
	template_name = 'inventario/entradas_form.html'
	success_url = reverse_lazy('inventario:entradas_list')


class EntradasDeleteView(LoginRequiredMixin, DeleteView):
	model = Entradas
	template_name = 'inventario/entradas_confirm_delete.html'
	success_url = reverse_lazy('inventario:entradas_list')

