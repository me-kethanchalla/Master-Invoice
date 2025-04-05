# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.inventory_list, name='inventory_list'),
    path('add/', views.add_inventory, name='add_inventory'),  # Ensure this URL pattern exists
    path('edit/<int:id>/', views.edit_inventory, name='edit_inventory'),
    path('delete/<int:id>/', views.delete_inventory, name='delete_inventory'),
    path('bulk-delete/', views.bulk_delete, name='bulk_delete'),
]
