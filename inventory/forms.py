from django import forms
from .models import Inventory


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [
            'product_name', 'item_id', 'quantity', 'cost_price', 'sale_price', 'max_retail_price', 'gst'
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Product name'
            }),
            'item_id': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Item ID'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Quantity'
            }),
            'cost_price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Cost price', 
                'step': '0.01'
            }),
            'sale_price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Sale price', 
                'step': '0.01'
            }),
            'max_retail_price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'MRP', 
                'step': '0.01'
            }),
            'gst': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'GST (below 100)', 
                'step': '0.01',
                'max': '100.00'  
            }),
        }


        
