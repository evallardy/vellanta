from django import forms
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class SolicitarCodigoForm(forms.Form):
    """Formulario para solicitar código de verificación"""
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            raise forms.ValidationError('No existe un usuario con este correo electrónico.')
        return email


class VerificarCodigoForm(forms.Form):
    """Formulario para verificar el código"""
    codigo = forms.CharField(
        max_length=6,
        label='Código de verificación',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000000',
            'maxlength': '6'
        })
    )


class NuevaContrasenaForm(forms.Form):
    """Formulario para establecer nueva contraseña"""
    password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '********'
        })
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '********'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
        if password1 and len(password1) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
        return cleaned_data


class UsuarioForm(forms.ModelForm):
    """Formulario para crear/editar usuarios"""
    password1 = forms.CharField(
        label='Contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '********',
            'autocomplete': 'new-password'
        }),
        help_text='Dejar en blanco para no cambiar la contraseña (solo al editar)'
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '********',
            'autocomplete': 'new-password'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limpiar los valores de contraseña al cargar el formulario
        if self.instance.pk:
            self.fields['password1'].initial = None
            self.fields['password2'].initial = None
    
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'materno', 'email', 
                  'celular', 'rol', 'talleres', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'materno': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'talleres': forms.CheckboxSelectMultiple(),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'username': 'Nombre de usuario para iniciar sesión',
            'email': 'Correo electrónico del usuario',
            'rol': 'Rol del usuario en el sistema',
            'talleres': 'Talleres a los que pertenece (solo para rol taller)',
            'is_active': 'Indica si el usuario puede iniciar sesión',
            'is_staff': 'Indica si el usuario puede acceder al admin',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        # Si es un nuevo usuario, la contraseña es obligatoria
        if not self.instance.pk and not password1:
            raise forms.ValidationError('La contraseña es obligatoria para nuevos usuarios.')
        
        # Si se ingresó contraseña, validar que coincidan
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError('Las contraseñas no coinciden.')
            if password1 and len(password1) < 8:
                raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
        return cleaned_data
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        
        # Solo actualizar contraseña si se proporcionó una nueva
        if password:
            usuario.set_password(password)
        
        if commit:
            usuario.save()
            self.save_m2m()
        
        return usuario
