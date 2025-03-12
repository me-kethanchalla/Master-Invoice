from django.db import models
from django.contrib.auth.models import User

class InvoiceBill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    date = models.DateField()
    bill_number = models.CharField(max_length=255)
    retailer_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Invoice {self.bill_number} - {self.user.username}"
    
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