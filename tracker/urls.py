from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('registrar/', views.registrar_actividad, name='registrar_actividad'),
    path('areas/', views.gestionar_areas, name='gestionar_areas'),
    path('areas/eliminar/<int:pk>/', views.eliminar_area, name='eliminar_area'),
    path('actividad/eliminar/<int:pk>/', views.eliminar_actividad, name='eliminar_actividad'),
    path('registro/', views.registro, name='registro'),
    path('areas/editar/<int:pk>/', views.editar_area, name='editar_area'),
]