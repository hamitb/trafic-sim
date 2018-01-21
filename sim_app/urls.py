from django.urls import path
from . import views

app_name = 'sim_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('settings/<str:component>/', views.settings, name='settings'),
    path('simulation/', views.simulation, name='simulation'),
    path('map_state/', views.map_state, name='map_state'),
]
