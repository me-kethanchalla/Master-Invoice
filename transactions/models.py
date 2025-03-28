from django.db import models
from inventory.models import Inventory
from inward_supply.models import Supplier
from outward_supply.models import Retailer
from datetime import date
from django.contrib.auth import get_user_model


User = get_user_model()
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    firm_name = models.CharField(max_length=255)
    person_name = models.CharField(max_length=255)
    add_date = models.DateField()
    payment = models.FloatField(default=0.0)
    remarks = models.CharField(max_length=1023)
    type = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.firm_name} - {self.person_name}"