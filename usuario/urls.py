from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    # Recuperación de contraseña
    path('recuperar-contrasena/', views.solicitar_codigo, name='solicitar_codigo'),
    path('verificar-codigo/', views.verificar_codigo, name='verificar_codigo'),
    path('nueva-contrasena/', views.nueva_contrasena, name='nueva_contrasena'),
    
    # CRUD de usuarios
    path('', views.UsuarioListView.as_view(), name='usuario_list'),
    path('add/', views.UsuarioCreateView.as_view(), name='usuario_add'),
    path('<int:pk>/edit/', views.UsuarioUpdateView.as_view(), name='usuario_edit'),
    path('<int:pk>/delete/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),
]
