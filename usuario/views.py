from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .forms import SolicitarCodigoForm, VerificarCodigoForm, NuevaContrasenaForm, UsuarioForm
from .password_reset import CodigoVerificacion

Usuario = get_user_model()


def solicitar_codigo(request):
    """Vista para solicitar código de verificación"""
    if request.method == 'POST':
        form = SolicitarCodigoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            usuario = Usuario.objects.get(email=email)
            
            # Crear y enviar código
            codigo = CodigoVerificacion.crear_codigo(usuario)
            if codigo.enviar_email():
                request.session['reset_user_id'] = usuario.id
                messages.success(request, f'Se ha enviado un código de verificación a {email}')
                return redirect('usuario:verificar_codigo')
            else:
                messages.error(request, 'Error al enviar el correo. Por favor, intenta de nuevo.')
    else:
        form = SolicitarCodigoForm()
    
    return render(request, 'usuario/solicitar_codigo.html', {'form': form})


def verificar_codigo(request):
    """Vista para verificar el código"""
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, 'Sesión expirada. Por favor, solicita un nuevo código.')
        return redirect('usuario:solicitar_codigo')
    
    if request.method == 'POST':
        form = VerificarCodigoForm(request.POST)
        if form.is_valid():
            codigo_ingresado = form.cleaned_data['codigo']
            
            try:
                usuario = Usuario.objects.get(id=user_id)
                codigo = CodigoVerificacion.objects.filter(
                    usuario=usuario,
                    codigo=codigo_ingresado,
                    usado=False
                ).latest('creado')
                
                if codigo.es_valido():
                    request.session['verified_code_id'] = codigo.id
                    return redirect('usuario:nueva_contrasena')
                else:
                    messages.error(request, 'El código ha expirado o ya fue usado. Solicita uno nuevo.')
            except CodigoVerificacion.DoesNotExist:
                messages.error(request, 'Código inválido.')
    else:
        form = VerificarCodigoForm()
    
    return render(request, 'usuario/verificar_codigo.html', {'form': form})


def nueva_contrasena(request):
    """Vista para establecer nueva contraseña"""
    code_id = request.session.get('verified_code_id')
    if not code_id:
        messages.error(request, 'Debes verificar tu código primero.')
        return redirect('usuario:solicitar_codigo')
    
    try:
        codigo = CodigoVerificacion.objects.get(id=code_id)
        if not codigo.es_valido():
            messages.error(request, 'El código ha expirado.')
            return redirect('usuario:solicitar_codigo')
    except CodigoVerificacion.DoesNotExist:
        messages.error(request, 'Código inválido.')
        return redirect('usuario:solicitar_codigo')
    
    if request.method == 'POST':
        form = NuevaContrasenaForm(request.POST)
        if form.is_valid():
            # Actualizar contraseña
            usuario = codigo.usuario
            usuario.set_password(form.cleaned_data['password1'])
            usuario.save()
            
            # Marcar código como usado
            codigo.usado = True
            codigo.save()
            
            # Limpiar sesión
            request.session.pop('reset_user_id', None)
            request.session.pop('verified_code_id', None)
            
            messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
            return redirect('login')
    else:
        form = NuevaContrasenaForm()
    
    return render(request, 'usuario/nueva_contrasena.html', {'form': form})


# CRUD de Usuarios
class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuario/usuario_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            return qs.filter(
                Q(username__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(materno__icontains=q) |
                Q(email__icontains=q)
            )
        return qs


class UsuarioCreateView(LoginRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/usuario_form.html'
    success_url = reverse_lazy('usuario:usuario_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuario creado exitosamente.')
        return super().form_valid(form)


class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/usuario_form.html'
    
    def get_success_url(self):
        # Si el usuario está editando su propia cuenta, redirigir al home
        if self.request.user.pk == self.object.pk:
            return reverse_lazy('home')
        # Si es administrador editando otro usuario, ir a la lista
        return reverse_lazy('usuario:usuario_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Determinar si es edición desde CRUD (administrador editando otros) o desde cuenta propia
        context['is_admin_editing'] = (
            self.request.user.rol == 'administrador' and 
            self.request.user.pk != self.object.pk
        )
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuario actualizado exitosamente.')
        return super().form_valid(form)


class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuario/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario:usuario_list')
    
    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Usuario eliminado exitosamente.')
        return super().post(request, *args, **kwargs)
