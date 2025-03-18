from django.contrib import admin
from .models import Supplier, InvoiceBill, ProductEntry

admin.site.register(Supplier)
admin.site.register(InvoiceBill)
admin.site.register(ProductEntry)