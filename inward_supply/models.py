from django.db import models
from django.contrib.auth.models import User
from inventory.models import Inventory
from django.contrib.auth import get_user_model

class InvoiceBill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    date = models.DateField()
    bill_number = models.CharField(max_length=255)
    supplier = models.ForeignKey("Supplier", on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"Invoice {self.bill_number} - {self.supplier.firm_name}"

    def get_total_amount(self):
        # Calculate total by summing (quantity * amount) for each product
        return sum(item.quantity * item.amount for item in self.products.all())
    
    def get_item_count(self):
        return self.products.count()

    
class ProductEntry(models.Model):
    invoice = models.ForeignKey(InvoiceBill, on_delete=models.CASCADE, related_name="products")
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()  # This is the unit price/amount per item
    
    def __str__(self):
        return f"{self.product_name} - {self.amount}"
    
    def get_total(self):
        return self.quantity * self.amount
   
User = get_user_model()
class Supplier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    firm_name = models.CharField(max_length=255)
    person_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, unique=True)
    email_id = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    debit = models.FloatField(default=0.0)
    total_sales = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.firm_name} ({self.person_name})"