from django.urls import path
from .views import add_supplier,view_suppliers,edit_supplier,add_invoice, invoice_list, invoice_detail

urlpatterns=[

    path('add-supplier/', add_supplier, name='add_supplier'),
    path('suppliers/', view_suppliers, name='view_suppliers'),
    path('edit-supplier/<int:pk>/', edit_supplier, name='edit_supplier'),

    path('add_invoice/',add_invoice, name='add-inward-bill'),
    path("", invoice_list, name="invoice_list"),
    path("invoices/<str:bill_number>/", invoice_detail, name="invoice_detail"),

]