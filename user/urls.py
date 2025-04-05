from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.user_login, name='login2'),
    path('home/', views.home, name ='home'),
    # path('welcome/', views.welcome, name='welcome'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('details/', views.details, name='details'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('logout/', views.user_logout, name='logout2'),
    path('forgot_password/', views.request_reset, name='forgot_password'),
    path('verify_reset/', views.verify_and_reset, name='verify_reset'),
    path('db-info/', views.db_info, name='db_info'),
]  
