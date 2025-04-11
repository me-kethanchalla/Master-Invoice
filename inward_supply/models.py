from django.db import models
from django.contrib.auth.models import User
from inventory.models import Inventory
from django.core.validators import MinLengthValidator
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
        return sum(item.amount for item in self.products.all())
    
    def get_item_count(self):
        return sum(item.quantity for item in self.products.all())
    class Meta:
        unique_together = ('user', 'bill_number')

    
class ProductEntry(models.Model):
    invoice = models.ForeignKey(InvoiceBill, on_delete=models.CASCADE, related_name="products")
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    amount = models.FloatField()  # This is the unit price*quantity per item
    
    def __str__(self):
        return f"{self.product_name} - {self.amount}"
    
    def unit_amount(self):
        return self.amount/self.quantity
   
User = get_user_model()
class Supplier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    firm_name = models.CharField(max_length=255)
    person_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email_id = models.EmailField()
    address = models.CharField(max_length=255)
    debit = models.FloatField(default=0.0)
    total_sales = models.FloatField(default=0)

    def __str__(self):
        return f"{self.firm_name} ({self.person_name})"
    
    class Meta:
        unique_together = ('user', 'firm_name')