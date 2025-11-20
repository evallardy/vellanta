from django.urls import path
from . import views

app_name = 'proveedor'

urlpatterns = [
    path('', views.ProveedorListView.as_view(), name='proveedor_list'),
    path('add/', views.ProveedorCreateView.as_view(), name='proveedor_add'),
    path('<int:pk>/edit/', views.ProveedorUpdateView.as_view(), name='proveedor_edit'),
    path('<int:pk>/delete/', views.ProveedorDeleteView.as_view(), name='proveedor_delete'),
]
