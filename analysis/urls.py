from django.urls import path
from . import views

urlpatterns = [
    path('get_suppliers_data/', views.get_top_suppliers, name='get_suppliers'),
    path('get_retailers_data/', views.get_top_retailers, name='get_retailers'),
    path('', views.view, name='view'),
    path('allsales/', views.allsales, name='allsales'),
]