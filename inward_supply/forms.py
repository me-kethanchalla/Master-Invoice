from django import forms

class InvoiceForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Enter Date'}))
    bill_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bill Number'}))
    retailer_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Retailer Name'}))