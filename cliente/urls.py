from django.urls import path
from . import views

app_name = 'cliente'

urlpatterns = [
    path('', views.ClienteListView.as_view(), name='cliente_list'),
    path('add/', views.ClienteCreateView.as_view(), name='cliente_add'),
    path('<int:pk>/edit/', views.ClienteUpdateView.as_view(), name='cliente_edit'),
    path('<int:pk>/delete/', views.ClienteDeleteView.as_view(), name='cliente_delete'),
]
