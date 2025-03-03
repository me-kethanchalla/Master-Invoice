# inward_supply/forms.py

from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['firm_name', 'person_name', 'phone_number', 'email_id', 'address']
        widgets = {
            'firm_name': forms.TextInput(attrs={'placeholder': 'Firm Name', 'class': 'form-control'}),
            'person_name': forms.TextInput(attrs={'placeholder': 'Person Name', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'email_id': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address', 'class': 'form-control', 'rows': 3}),
        }
