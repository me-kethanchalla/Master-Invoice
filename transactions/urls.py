
from django.urls import path
from . import views
urlpatterns=[
 path('add_outward_transaction/',views.add_outward_transaction, name='add_outward_transaction'),
 path('add_inward_transaction/',views.add_inward_transaction, name='add_inward_transaction'),
 path("pending/", views.pending, name="pending"),
 path("view_transaction_history/", views.view_transaction_history, name="view_transaction_history"),
 path("update_transaction_supplier/", views.update_transaction_supplier, name="update_transaction_supplier"),
 path("update_transaction_retailer/", views.update_transaction_retailer, name="update_transaction_retailer"),
]