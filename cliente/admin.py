from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'razon_social', 'rfc', 'telefono', 'email', 'activo', 'creado')
    search_fields = ('nombre', 'razon_social', 'rfc', 'email')
    list_filter = ('activo',)
from django.contrib import admin

# Register your models here.
