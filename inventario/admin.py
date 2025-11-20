from django.contrib import admin
from .models import MarcaLlanta, Llanta, Inventario, Entradas


@admin.register(MarcaLlanta)
class MarcaLlantaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'creado')
    search_fields = ('nombre',)


@admin.register(Llanta)
class LlantaAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'ancho', 'alto', 'rin', 'radial', 'creado')
    list_filter = ('marca',)
    search_fields = ('modelo', 'ancho', 'alto', 'rin')


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'empresa', 'producto_clave', 'existencia', 'precio', 'estatus')
    list_filter = ('estatus', 'marca')
    search_fields = ('descripcion', 'producto_clave')


@admin.register(Entradas)
class EntradasAdmin(admin.ModelAdmin):
    list_display = ('talleres', 'llantas', 'producto_clave', 'cantidad', 'precio')
    list_filter = ('talleres',)
    search_fields = ('producto_clave', 'llantas__modelo')

from django.contrib import admin

# Register your models here.
