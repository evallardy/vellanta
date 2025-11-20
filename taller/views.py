from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Taller
from .forms import TallerForm


class TallerListView(ListView):
    model = Taller
    template_name = 'taller/taller_list.html'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            return qs.filter(
                Q(id_empresa__icontains=q) |
                Q(razon_social__icontains=q) |
                Q(municipio__icontains=q) |
                Q(estado__icontains=q)
            )
        return qs


class TallerCreateView(LoginRequiredMixin, CreateView):
    model = Taller
    form_class = TallerForm
    template_name = 'taller/taller_form.html'
    success_url = reverse_lazy('taller:taller_list')


class TallerUpdateView(LoginRequiredMixin, UpdateView):
    model = Taller
    form_class = TallerForm
    template_name = 'taller/taller_form.html'
    success_url = reverse_lazy('taller:taller_list')


class TallerDeleteView(LoginRequiredMixin, DeleteView):
    model = Taller
    template_name = 'taller/taller_confirm_delete.html'
    success_url = reverse_lazy('taller:taller_list')
