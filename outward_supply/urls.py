from django.urls import path
from .views import add_retailer,view_retailers, edit_retailer, add_out_invoice, out_invoice_list, out_invoice_detail

urlpatterns = [
    path('add-retailer/', add_retailer, name='add_retailer'),
    path('retailers/', view_retailers, name='view_retailers'),
    path('edit-retailer/<int:pk>/', edit_retailer, name='edit_retailer'),

    path('add_out_invoice/',add_out_invoice, name='add-outward-bill'),
    path("", out_invoice_list, name="out_invoice_list"), 
    path("outinvoices/<str:bill_number>/", out_invoice_detail, name="out_invoice_detail"),
]