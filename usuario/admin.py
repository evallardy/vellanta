
from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
	list_display = ("username", "first_name", "last_name", "materno", "celular", "email", "rol", "is_staff")
