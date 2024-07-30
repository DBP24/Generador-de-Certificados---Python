from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns =[
    path('', views.dashboard, name='dashboard'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]