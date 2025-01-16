from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name = 'blogg_home'),
    path('home/', views.welcome, name ='blogg_welcome'),
]