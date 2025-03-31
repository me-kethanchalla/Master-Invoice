from django.db import models
from inventory.models import Inventory
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()

class Retailer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    firm_name = models.CharField(max_length=255)
    person_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)]
    )
    email_id = models.EmailField()
    address = models.CharField(max_length=255)
    credit = models.FloatField(default=0.0)
    total_sales = models.FloatField(default=0)

    def __str__(self):
        return f"{self.firm_name} ({self.person_name})"
    
class Outward_Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    bill_number = models.CharField(max_length=255)
    retailer = models.ForeignKey("Retailer", on_delete=models.CASCADE, null=True, blank=True)
    discount = models.FloatField(default=0.0)
    profit = models.FloatField(default=0.0)

    def __str__(self):
        if self.retailer:
            return f"Invoice {self.bill_number} - {self.retailer.firm_name}"
        return f"Invoice {self.bill_number}"

    def get_total_amount(self):
        total = sum(item.amount for item in self.products.all())
        return total * (1 - self.discount / 100)

    def get_item_count(self):
        return sum(item.quantity for item in self.products.all())

    def get_total_profit(self):
        return sum(item.quantity * item.profit for item in self.products.all())
    class Meta:
        unique_together = ('user', 'bill_number')
    
class ProductEntry(models.Model):
    invoice = models.ForeignKey(Outward_Invoice, on_delete=models.CASCADE, related_name="products")
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    amount = models.FloatField()  # This is the unit price*quantity per item
    
    def __str__(self):
        return f"{self.product_name} - {self.amount}"
    
    def unit_amount(self):
        return self.amount / self.quantity