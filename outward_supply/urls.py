from django.urls import path
from .views import add_retailer,view_retailers, edit_retailer

urlpatterns = [
    path('add-retailer/', add_retailer, name='add_retailer'),
    path('retailers/', view_retailers, name='view_retailers'),
    path('edit-retailer/<int:pk>/', edit_retailer, name='edit_retailer'),
]