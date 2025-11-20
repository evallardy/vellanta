from django import forms
from .models import MarcaLlanta, Llanta, Inventario, Entradas


class MarcaLlantaForm(forms.ModelForm):
    class Meta:
        model = MarcaLlanta
        fields = ['nombre']
        help_texts = {
            'nombre': 'Nombre de la marca (ej. Michelin)',
        }


class LlantaForm(forms.ModelForm):
    class Meta:
        model = Llanta
        fields = ['marca', 'modelo', 'ancho', 'alto', 'rin', 'radial']
        help_texts = {
            'modelo': 'Modelo de la llanta.',
            'ancho': 'Ancho en mm (ej. 205).',
            'alto': 'Perfil o alto en porcentaje (ej. 55).',
            'rin': 'Rin en pulgadas (ej. 16).',
        }


class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['id_inventario', 'empresa', 'producto_clave', 'descripcion', 'marca', 'ancho', 'alto', 'rin', 'existencia', 'precio', 'estatus', 'imagen', 'imagen1']
        help_texts = {
            'id_inventario': 'Identificador único interno.',
            'producto_clave': 'Clave o SKU del producto.',
            'descripcion': 'Descripción breve del producto.',
            'existencia': 'Cantidad disponible en stock.',
            'precio': 'Precio de venta (moneda local).',
        }


class EntradasForm(forms.ModelForm):
    class Meta:
        model = Entradas
        fields = ['talleres', 'llantas', 'producto_clave', 'precio', 'cantidad']
        help_texts = {
            'talleres': 'Selecciona el taller receptor.',
            'llantas': 'Selecciona la llanta asociada.',
            'producto_clave': 'Clave relacionada al inventario.',
            'cantidad': 'Número de unidades ingresadas.',
        }

