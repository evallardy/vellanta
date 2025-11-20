from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'razon_social', 'rfc', 'telefono', 'email', 'direccion', 'activo']
        help_texts = {
            'rfc': 'RFC si aplica (opcional).',
            'telefono': 'Teléfono de contacto.',
            'email': 'Correo electrónico de contacto.',
        }