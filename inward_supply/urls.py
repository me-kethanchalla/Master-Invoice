from django.urls import path
from . import views

urlpatterns=[
    path('add_invoice/',views.add_invoice, name='add-inward-bill'),
    path("", views.invoice_list, name="invoice_list"),
    path("invoices/<str:bill_number>/", views.invoice_detail, name="invoice_detail"),
]