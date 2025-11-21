from django import forms
from .models import Taller
from usuario.models import Usuario


class TallerForm(forms.ModelForm):
    usuarios = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.filter(rol='taller'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Usuarios del Taller',
        help_text='Selecciona los usuarios que pertenecen a este taller.'
    )
    
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['usuarios'].initial = self.instance.usuarios.all()
    
    def save(self, commit=True):
        taller = super().save(commit=commit)
        if commit:
            taller.usuarios.set(self.cleaned_data['usuarios'])
        return taller
