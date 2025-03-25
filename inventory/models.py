from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to Django User model
    product_name = models.CharField(max_length=255)
    item_id = models.CharField(max_length=50)  # Unique identifier for item
    quantity = models.PositiveIntegerField()  # Available quantity
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)  # Cost price
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)  # Sale price
    max_retail_price = models.DecimalField(max_digits=10, decimal_places=2)  # MRP
    gst = models.DecimalField(max_digits=5, decimal_places=2)  # GST percentage
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Profit per item
    total_qty_sold = models.PositiveIntegerField(default=0)  # Total items sold

    def save(self, *args, **kwargs):
        # Ensure values are Decimal before performing calculations
        self.sale_price = Decimal(self.sale_price)
        self.cost_price = Decimal(self.cost_price)
        
        # Calculate profit (profit per item = sale price - cost price)
        self.profit = self.sale_price - self.cost_price
        
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.product_name} ({self.item_id}) - Qty: {self.quantity}"
    
    class Meta:
        unique_together = ('user', 'item_id')

