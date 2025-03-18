
from django.urls import path
from . import views
urlpatterns=[
 path('clear_retailer_debit/',views.clear_retailer_debit, name='clear_retailer_debit'),
 path('clear_supplier_debit/',views.clear_supplier_debit, name='clear_supplier_debit'),
 path("pending/", views.pending, name="pending"),
 path("view_transaction_history/", views.view_transaction_history, name="view_transaction_history"),
 path("update_transaction_supplier/", views.update_transaction_supplier, name="update_transaction_supplier"),
 path("update_transaction_retailer/", views.update_transaction_retailer, name="update_transaction_retailer"),
]