from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    product_name = models.CharField(max_length=255)
    item_id = models.CharField(max_length=50)  
    quantity = models.PositiveIntegerField()  
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)  
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)  
    max_retail_price = models.DecimalField(max_digits=10, decimal_places=2)  
    gst = models.DecimalField(max_digits=5, decimal_places=2)  
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    total_qty_sold = models.PositiveIntegerField(default=0)  

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

