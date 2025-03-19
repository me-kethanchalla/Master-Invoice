from django.shortcuts import render, redirect, get_object_or_404
from .forms import SupplierForm, InvoiceForm
from .models import InvoiceBill, ProductEntry, Supplier
from django.db.models import Q
from django.contrib.auth.decorators import login_required


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

@login_required
def add_invoice(request):
    supplier = Supplier.objects.all()
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            
            invoice = InvoiceBill(
                user=request.user,
                date=form.cleaned_data['date'],
                bill_number=form.cleaned_data['bill_number'],
                retailer_name=form.cleaned_data['retailer_name']
            )
            invoice.save()
            
            products = request.POST.getlist('product[]')
            quantities = request.POST.getlist('quantity[]')
            amounts = request.POST.getlist('amount[]')
            
            
            for i in range(len(products)):
                if i < len(quantities) and i < len(amounts) and products[i].strip():
                    ProductEntry.objects.create(
                        invoice=invoice,
                        product_name=products[i],
                        quantity=int(quantities[i]),
                        amount=int(amounts[i])
                    )
            
            return redirect('invoice_list')
    else:
        form = InvoiceForm()
    
    return render(request, "inward_supply/invoice_form.html", {"form": form, 'supplier': supplier})

@login_required
def invoice_list(request):
    invoices = InvoiceBill.objects.filter(user=request.user)
    return render(request, "inward_supply/view_bill.html", {"invoices": invoices})

@login_required
def invoice_detail(request, bill_number):
    invoice = get_object_or_404(InvoiceBill, bill_number=bill_number, user=request.user)
    return render(request, "inward_supply/invoice_detail.html", {"invoice": invoice})
