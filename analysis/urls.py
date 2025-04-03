from django.urls import path
from . import views

urlpatterns = [
    path('get_suppliers_data/', views.get_top_suppliers, name='get_suppliers'),
    path('get_retailers_data/', views.get_top_retailers, name='get_retailers'),
    path('', views.view, name='analysis_graphs'),
    path('allsales/', views.allsales, name='allsales'),
    path('get_profits_data/', views.get_profit, name='get_profit'),
    path('get_sales_data/', views.get_sales, name='get_sales'),
    path('get_bills_data/', views.outward_invoice_bill, name="get_invoicebills"),
    path('get_transaction_data/', views.inward_transaction, name="get_transactions"),
]