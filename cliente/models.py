from django.db import models


class Cliente(models.Model):
	nombre = models.CharField('Nombre', max_length=150)
	razon_social = models.CharField('Razón social', max_length=200, blank=True, null=True)
	rfc = models.CharField('RFC', max_length=20, blank=True, null=True)
	telefono = models.CharField('Teléfono', max_length=30, blank=True, null=True)
	email = models.EmailField('Email', blank=True, null=True)
	direccion = models.TextField('Dirección', blank=True, null=True)
	activo = models.BooleanField('Activo', default=True)
	creado = models.DateTimeField('Creado', auto_now_add=True)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = 'Cliente'
		verbose_name_plural = 'Clientes'
		ordering = ['nombre']
		db_table = 'Cliente'
