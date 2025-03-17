from django.urls import path
from .views import add_supplier,view_suppliers,edit_supplier

urlpatterns = [
    path('add-supplier/', add_supplier, name='add_supplier'),
    path('suppliers/', view_suppliers, name='view_suppliers'),
    path('edit-supplier/<int:pk>/', edit_supplier, name='edit_supplier'),
]
