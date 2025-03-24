from django.contrib import admin
from .models import Retailer, Outward_Invoice, ProductEntry

admin.site.register(Retailer)
admin.site.register(Outward_Invoice)
admin.site.register(ProductEntry)