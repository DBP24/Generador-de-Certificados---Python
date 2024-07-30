from django.urls import path

from . import views

app_name = 'certificate'

urlpatterns =[
    path('', views.brind_dat, name='cargar'),
  
]