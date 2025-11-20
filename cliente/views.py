from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cliente
from .forms import ClienteForm


class ClienteListView(ListView):
    model = Cliente
    template_name = 'cliente/cliente_list.html'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            return qs.filter(nombre__icontains=q)
        return qs


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/cliente_form.html'
    success_url = reverse_lazy('cliente:cliente_list')


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/cliente_form.html'
    success_url = reverse_lazy('cliente:cliente_list')


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'cliente/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente:cliente_list')
from django.shortcuts import render

# Create your views here.
