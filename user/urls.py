from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_view
from django.contrib import admin

urlpatterns = [
    path('', views.user_login, name='login2'),
    path('home/', views.home, name ='home'),
]  