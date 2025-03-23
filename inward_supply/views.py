from django.shortcuts import render, redirect, get_object_or_404
from .forms import SupplierForm, InvoiceForm
from .models import InvoiceBill, ProductEntry, Supplier, Inventory
from decimal import Decimal
import json
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime

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

    message = ""
    # Fetch suppliers for the logged-in user
    suppliers = Supplier.objects.filter(user=request.user)
    
    # Fetch all products from the Inventory model
    products = Inventory.objects.all()
    
    # Serialize product data for JavaScript usage
    product_data = []
    for p in products:
        product_data.append({
            'id': p.id,
            'name': p.product_name,
            'sale_price': float(p.sale_price),
            'gst': float(p.gst),  # e.g., 18.0 means 18%
        })
    productJSON = json.dumps(product_data)
    
    if request.method == 'POST':
        print("POST received")
        form = InvoiceForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            # Use manual values from the form
            invoice = InvoiceBill(
                user=request.user,
                date=form.cleaned_data['date'],
                bill_number=form.cleaned_data['bill_number'],
            )
            # Retrieve the selected supplier from the dropdown (name="billed-to")
            selected_supplier_id = request.POST.get('billed-to')
            if selected_supplier_id:
                invoice.supplier = get_object_or_404(Supplier, id=selected_supplier_id, user=request.user)
            invoice.save()
            
            # Process product rows
            product_ids = request.POST.getlist('product_id[]')
            quantities = request.POST.getlist('quantity[]')
            invoice_total = Decimal('0.00')
            total_items = 0  # To count total items sold
            
            for i in range(len(product_ids)):
                if i < len(quantities) and product_ids[i].strip():
                    product_obj = get_object_or_404(Inventory, id=product_ids[i])
                    try:
                        quantity_val = int(quantities[i])
                    except ValueError:
                        quantity_val = 0
                    
                    sale_price = product_obj.sale_price
                    gst = product_obj.gst
                    
                    # Calculate total amount
                    total_amount = (sale_price * Decimal(quantity_val)) * (1 + (gst / Decimal(100)))
                    
                    # Create a product entry
                    ProductEntry.objects.create(
                        invoice=invoice,
                        product_name=product_obj.product_name,
                        quantity=quantity_val,
                        amount=total_amount
                    )
                    
                    # Update the quantity in inventory
                    
                    product_obj.quantity += quantity_val
                    product_obj.save()

                    invoice_total += total_amount
                    total_items += quantity_val

            
            # Update supplier's debit and total sales if supplier exists
            if invoice.supplier:
                invoice.supplier.debit += float(invoice_total)
                invoice.supplier.total_sales += total_items
                invoice.supplier.save()
            
            message = "Invoice is added successfully!"
            return redirect('invoice_list')
        else:
            print("Form errors:", form.errors)
    else:
        form = InvoiceForm()
    
    return render(request, "inward_supply/invoice_form.html", {
        "form": form,
        "suppliers": suppliers,
        "productJSON": productJSON,
        "message": message
    })



@login_required
def invoice_list(request):
    query = request.GET.get('query', '')
    invoices = InvoiceBill.objects.filter(user=request.user)
    
    if query:
        try:
            # Try to parse the query as a date (format: YYYY-MM-DD)
            query_date = datetime.strptime(query, '%Y-%m-%d').date()
            invoices = invoices.filter(date=query_date)
        except ValueError:
            # If not a date, search by supplier firm name or bill number
            invoices = invoices.filter(
                Q(supplier__firm_name__icontains=query) |
                Q(bill_number__icontains=query)
            )
    
    return render(request, "inward_supply/view_bill.html", {"invoices": invoices})

@login_required
def invoice_detail(request, bill_number):
    invoice = get_object_or_404(InvoiceBill, bill_number=bill_number, user=request.user)
    return render(request, "inward_supply/invoice_detail.html", {"invoice": invoice})


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