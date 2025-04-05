from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .models import Supplier

class InvoiceForm(forms.Form):
    date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Enter Date'})
    )
    bill_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bill Number'})
    )

    


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
