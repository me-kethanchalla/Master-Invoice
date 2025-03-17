from django.urls import path
from . import views

urlpatterns=[
    path('clear_retailer_debit/',views.clear_retailer_debit, name='clear_retailer_debit'),
    path('clear_supplier_debit/',views.clear_supplier_debit, name='clear_supplier_debit'),
    path("pending/", views.pending, name="pending"),
]