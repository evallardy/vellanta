from django.contrib import admin
from .models import Taller


@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
	list_display = ('id_empresa', 'razon_social', 'municipio', 'estado', 'telefono', 'creado')
	search_fields = ('id_empresa', 'razon_social', 'municipio', 'estado')
	list_filter = ('estado', 'municipio')
