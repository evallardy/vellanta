
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
	materno = models.CharField(max_length=150, blank=True)
	celular = models.CharField(max_length=20, blank=True)

	# Rol dentro del sistema: cliente, proveedor o administrador
	ROL_CHOICES = (
		('cliente', 'Cliente'),
		('taller', 'Taller'),
		('proveedor', 'Proveedor'),
		('administrador', 'Administrador'),
	)
	rol = models.CharField('Rol', max_length=20, choices=ROL_CHOICES, default='cliente')

	class Meta:
		verbose_name = 'Usuario'
		verbose_name_plural = 'Usuarios'
		ordering = ['last_name','materno','first_name']
		db_table = 'Usuario'

	def __str__(self):
		return f"{self.first_name} {self.last_name} {self.materno}".strip()
    
    

