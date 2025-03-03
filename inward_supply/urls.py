from django.urls import path
from .views import add_supplier,view_suppliers

urlpatterns = [
    path('add-supplier/', add_supplier, name='add_supplier'),
    path('suppliers/', view_suppliers, name='view_suppliers'),
]
