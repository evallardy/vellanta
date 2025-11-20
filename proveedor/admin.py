from django.contrib import admin
from .models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'razon_social', 'rfc', 'telefono', 'email', 'activo', 'creado')
    search_fields = ('nombre', 'razon_social', 'rfc', 'email')
    list_filter = ('activo',)
