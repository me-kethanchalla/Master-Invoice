from django.db import models
from inventory.models import Product
from django.contrib.auth import get_user_model

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

class InwardInvoiceBill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    bill_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateField()
    product_list = models.ManyToManyField(Product)
    final_amount = models.FloatField()

    def __str__(self):
        return f"Bill {self.bill_number} - {self.supplier.name}"

