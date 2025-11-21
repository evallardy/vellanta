
from django.contrib import admin
from .models import Usuario
from .password_reset import CodigoVerificacion

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
	list_display = ("username", "first_name", "last_name", "materno", "celular", "email", "rol", "is_staff")
	filter_horizontal = ('talleres',)


@admin.register(CodigoVerificacion)
class CodigoVerificacionAdmin(admin.ModelAdmin):
	list_display = ("usuario", "codigo", "creado", "usado", "es_valido")
	list_filter = ("usado", "creado")
	search_fields = ("usuario__username", "usuario__email", "codigo")
	readonly_fields = ("creado",)
