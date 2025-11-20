from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Proveedor
from .forms import ProveedorForm


class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'proveedor/proveedor_list.html'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            return qs.filter(nombre__icontains=q)
        return qs


class ProveedorCreateView(LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/proveedor_form.html'
    success_url = reverse_lazy('proveedor:proveedor_list')


class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/proveedor_form.html'
    success_url = reverse_lazy('proveedor:proveedor_list')


class ProveedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Proveedor
    template_name = 'proveedor/proveedor_confirm_delete.html'
    success_url = reverse_lazy('proveedor:proveedor_list')
