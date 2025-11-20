from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('marcas/', views.MarcaListView.as_view(), name='marca_list'),
    path('llantas/', views.LlantaListView.as_view(), name='llanta_list'),
    path('llantas/add/', views.LlantaCreateView.as_view(), name='llanta_add'),
    path('llantas/<int:pk>/edit/', views.LlantaUpdateView.as_view(), name='llanta_edit'),
    path('llantas/<int:pk>/delete/', views.LlantaDeleteView.as_view(), name='llanta_delete'),
    path('inventario/', views.InventarioListView.as_view(), name='inventario_list'),
    path('inventario/add/', views.InventarioCreateView.as_view(), name='inventario_add'),
    path('inventario/<int:pk>/edit/', views.InventarioUpdateView.as_view(), name='inventario_edit'),
    path('inventario/<int:pk>/delete/', views.InventarioDeleteView.as_view(), name='inventario_delete'),
    # Entradas
    path('entradas/', views.EntradasListView.as_view(), name='entradas_list'),
    path('entradas/add/', views.EntradasCreateView.as_view(), name='entradas_add'),
    path('entradas/<int:pk>/edit/', views.EntradasUpdateView.as_view(), name='entradas_edit'),
    path('entradas/<int:pk>/delete/', views.EntradasDeleteView.as_view(), name='entradas_delete'),
]
