from django import forms
from .models import Taller


class TallerForm(forms.ModelForm):
    class Meta:
        model = Taller
        fields = ['id_empresa', 'razon_social', 'direccion', 'numero_exterior', 'numero_interior', 
                  'colonia', 'codigo_postal', 'municipio', 'estado', 'telefono', 
                  'longitud', 'latitud', 'estatus', 'imagen']
        help_texts = {
            'id_empresa': 'Identificador único del taller.',
            'razon_social': 'Razón social del taller.',
            'telefono': 'Teléfono de contacto.',
            'imagen': 'Imagen del taller (opcional).',
        }
