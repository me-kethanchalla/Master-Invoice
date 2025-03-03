from django.urls import path
from .views import add_retailer,view_retailers

urlpatterns = [
    path('add-retailer/', add_retailer, name='add_retailer'),
    path('retailers/', view_retailers, name='view_retailers'),
]