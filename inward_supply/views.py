from django.shortcuts import render, redirect, get_object_or_404
from .forms import InvoiceForm
from .models import InvoiceBill, ProductEntry

def add_invoice(request):
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
    
    return render(request, "inward_supply/invoice_form.html", {"form": form})

def invoice_list(request):
    invoices = InvoiceBill.objects.filter(user=request.user)
    return render(request, "inward_supply/view_bill.html", {"invoices": invoices})

def invoice_detail(request, bill_number):
    invoice = get_object_or_404(InvoiceBill, bill_number=bill_number, user=request.user)
    return render(request, "inward_supply/invoice_detail.html", {"invoice": invoice})