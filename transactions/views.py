from django.shortcuts import render, get_object_or_404, redirect
from inventory.models import Inventory
from inward_supply.models import Supplier
from outward_supply.models import Retailer

def pending(request):
    suppliers = Supplier.objects.all()
    retailers = Retailer.objects.all()
    return render(request, 'transactions/pending.html', {'suppliers': suppliers, 'retailers': retailers})
def clear_retailer_debit(request):
    retailers = Retailer.objects.all()
    return render(request, 'transactions/clear_retailer_debit.html',{'retailers': retailers})
def clear_supplier_debit(request):
    suppliers = Supplier.objects.all()
    return render(request, 'transactions/clear_supplier_debit.html', {'suppliers': suppliers})