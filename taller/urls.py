from django.urls import path
from . import views

app_name = 'taller'

urlpatterns = [
    path('', views.TallerListView.as_view(), name='taller_list'),
    path('add/', views.TallerCreateView.as_view(), name='taller_add'),
    path('<int:pk>/edit/', views.TallerUpdateView.as_view(), name='taller_edit'),
    path('<int:pk>/delete/', views.TallerDeleteView.as_view(), name='taller_delete'),
]
