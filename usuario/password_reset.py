import random
import string
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.core.mail import send_mail
from django.conf import settings


class CodigoVerificacion(models.Model):
    """Modelo para almacenar códigos de verificación temporales"""
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6)
    creado = models.DateTimeField(auto_now_add=True)
    usado = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'CodigoVerificacion'
        verbose_name = 'Código de Verificación'
        verbose_name_plural = 'Códigos de Verificación'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.codigo}"
    
    def es_valido(self):
        """Verifica si el código sigue siendo válido (15 minutos)"""
        tiempo_limite = timezone.now() - timedelta(minutes=15)
        return not self.usado and self.creado > tiempo_limite
    
    @staticmethod
    def generar_codigo():
        """Genera un código aleatorio de 6 dígitos"""
        return ''.join(random.choices(string.digits, k=6))
    
    @classmethod
    def crear_codigo(cls, usuario):
        """Crea un nuevo código de verificación para el usuario"""
        # Invalidar códigos anteriores
        cls.objects.filter(usuario=usuario, usado=False).update(usado=True)
        
        # Crear nuevo código
        codigo = cls.generar_codigo()
        return cls.objects.create(usuario=usuario, codigo=codigo)
    
    def enviar_email(self):
        """Envía el código por correo electrónico"""
        asunto = 'Código de Verificación - Rueda Visión'
        mensaje = f"""
Hola {self.usuario.first_name},

Has solicitado restablecer tu contraseña en Rueda Visión.

Tu código de verificación es: {self.codigo}

Este código es válido por 15 minutos.

Si no solicitaste este cambio, ignora este mensaje.

Saludos,
Equipo de Rueda Visión
        """
        
        try:
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [self.usuario.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Error al enviar email: {e}")
            return False
