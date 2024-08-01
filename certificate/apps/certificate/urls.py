from django.urls import path

from . import views

app_name = 'certificate'

urlpatterns =[
    path('', views.brind_dat, name='cargar'),
    path('certificates/', views.recuper, name='recuperar'),
    path('certificados/', views.listCertificate, name='list_certificates'),
    path('certificados/download/<str:filename>/', views.download_certificate, name='download_certificate'),
]