from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SupplierForm
from .models import Supplier
from django.db.models import Q

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

@login_required
def view_suppliers(request):
    query = request.GET.get('query', '')
    if query:
        suppliers = Supplier.objects.filter(
            (Q(person_name__icontains=query) | Q(firm_name__icontains=query)),
            user=request.user
        )
    else:
        suppliers = Supplier.objects.filter(user=request.user)
    
    return render(request, 'inward_supply/view_suppliers.html', {'suppliers': suppliers})

@login_required
def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk, user=request.user)
    message = ""
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            message = "Supplier updated successfully!"
            return redirect('view_suppliers')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'inward_supply/edit_supplier.html', {'form': form, 'message': message, 'supplier': supplier})
