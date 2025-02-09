from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    item_id = models.CharField(max_length=50, unique=True)
    sales_price = models.FloatField()
    cost_price = models.FloatField()
    MRP = models.FloatField()
    gst = models.FloatField()
    quantity = models.IntegerField()
    profit = models.FloatField()
    total_quantity_sold = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product_name} - {self.company}"
