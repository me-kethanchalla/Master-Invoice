from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SupplierForm
from .models import Supplier

@login_required
def add_supplier(request):
    message = ""
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.user = request.user
            supplier.save()
            message = "Supplier added successfully!"
            # Reset the form by creating a new instance
            form = SupplierForm()
    else:
        form = SupplierForm()
    return render(request, 'inward_supply/add_supplier.html', {'form': form, 'message': message})

def view_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inward_supply/view_suppliers.html', {'suppliers': suppliers})













