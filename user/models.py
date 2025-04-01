from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firm_name = models.CharField(max_length=255, blank=False, null=False, default="")
    full_name = models.CharField(max_length=255, blank=False, null=False, default="")
    phone = models.CharField(max_length=10, blank=False, null=False, default="")
    address = models.TextField(blank=False, null=False, default="")
    GST_number = models.CharField(max_length=15, blank=False, null=False, default="")
    def __str__(self):
        return self.full_name or self.user.username

