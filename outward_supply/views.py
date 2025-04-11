from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RetailerForm, OutwardInvoiceForm
from .models import Retailer, Inventory, Outward_Invoice, ProductEntry
from django.db.models import Q
from decimal import Decimal
import json
from datetime import datetime, date
from user.models import Profile

@login_required
def add_retailer(request):
    message = ""
    if request.method == 'POST':
        print("POST recivied")
        form = RetailerForm(request.POST)
        if form.is_valid():
            print("Form valid")
            retailer = form.save(commit=False)
            retailer.user = request.user
            # Check for unique constraint violation
            if Retailer.objects.filter(user=request.user, firm_name=retailer.firm_name).exists():
                message = "Retailer with this Firm Name already exists for your account."
                message_type = "error"
            # Check for phone number length and all are digits
            elif len(retailer.phone_number) != 10 or not retailer.phone_number.isdigit():
                message = "Phone number must be 10 digits."
                message_type = "error"
            else:
                # Save the retailer instance
                retailer.save()
                message = "Retailer added successfully!"
                message_type = "success"
                # Reset the form by creating a new instance
                form = RetailerForm()
        else:
            print("Form errors:", form.errors)
    else:
        form = RetailerForm()
    return render(request, 'outward_supply/add_retailer.html', {'form': form, 'message': message})

@login_required
def view_retailers(request):
    query = request.GET.get('query', '')
    if query:
        retailers = Retailer.objects.filter(
            (Q(person_name__icontains=query) | Q(firm_name__icontains=query)),
            user=request.user
        )
    else:
        retailers = Retailer.objects.filter(user=request.user)

    return render(request, 'outward_supply/view_retailers.html', {'retailers': retailers})

@login_required
def edit_retailer(request, pk):
    retailer = get_object_or_404(Retailer, pk=pk, user=request.user)
    message = ""
    if request.method == "POST":
        form = RetailerForm(request.POST, instance=retailer)
        if form.is_valid():
            form.save()
            message = "Retailer updated successfully!"
            return redirect('view_retailers')
    else:
        form = RetailerForm(instance=retailer)
    return render(request, 'outward_supply/edit_retailer.html', {'form': form, 'message': message, 'retailer': retailer})

@login_required
def add_out_invoice(request):
    message = ""
    # Fetch retailers for the logged-in user
    retailers = Retailer.objects.filter(user=request.user)
    
    # Fetch all products from the Inventory model
    products = Inventory.objects.filter(user=request.user)
    
    # Serialize product data for JavaScript usage
    product_data = [
        {
            'id': p.id,
            'name': p.product_name,
            'sale_price': float(p.sale_price),
            'gst': float(p.gst),
            'available': p.quantity  # Include available quantity
        }
        for p in products
    ]
    productJSON = json.dumps(product_data)
    
    if request.method == 'POST':
        print("POST received")
        form = OutwardInvoiceForm(request.POST)
        if form.is_valid():
            bill_number = form.cleaned_data['bill_number']
            invoice_date = form.cleaned_data['date']
            discount_value = form.cleaned_data['discount']

            # Check for future date
            if invoice_date > date.today():
                form.add_error('date', "Invalid date entered. Future dates are not allowed.")
                return render(request, "outward_supply/add_outward_invoice.html", {
                    "form": form,
                    "retailers": retailers,
                    "productJSON": productJSON,
                    "message": "Error: Invalid Date"
                })

            #  Check for duplicate bill number BEFORE saving
            if Outward_Invoice.objects.filter(user=request.user, bill_number=bill_number).exists():
                form.add_error('bill_number', "Bill number already exists. Please use a unique bill number.")
                return render(request, "outward_supply/add_outward_invoice.html", {
                    "form": form,
                    "retailers": retailers,
                    "productJSON": productJSON,
                    "message": "Error: Duplicate Bill Number"
                })
            
            # Validate discount before creating the invoice
            if discount_value >= 100:
                form.add_error('discount', "Discount cannot be 100 or more.")
                return render(request, "outward_supply/add_outward_invoice.html", {
                    "form": form,
                    "retailers": retailers,
                    "productJSON": productJSON,
                    "message": "Discount should be less than 100%"
                })

            # Pre-check: Validate stock
            product_ids = request.POST.getlist('product_id[]')
            quantities = request.POST.getlist('quantity[]')
            stock_errors = []
            for product_id, quantity in zip(product_ids, quantities):
                if product_id.strip() and quantity.strip():
                    product_obj = get_object_or_404(Inventory, id=product_id, user=request.user)
                    try:
                        quantity_val = int(quantity)
                    except ValueError:
                        quantity_val = 0
                    if product_obj.quantity < quantity_val:
                        stock_errors.append(
                            f"Not enough stock for {product_obj.product_name} (Available: {product_obj.quantity}, requested: {quantity_val})."
                        )

            if stock_errors:
                form.add_error(None, " ".join(stock_errors))
                return render(request, "outward_supply/add_outward_invoice.html", {
                    "form": form,
                    "retailers": retailers,
                    "productJSON": productJSON,
                    "message": "Error: " + " ".join(stock_errors)
                })

            # Passed all checks, now create invoice
            retailer_id = request.POST.get('billed-to')
            retailer_obj = get_object_or_404(Retailer, id=retailer_id, user=request.user) if retailer_id else None

            invoice = Outward_Invoice.objects.create(
                user=request.user,
                date=invoice_date,
                bill_number=bill_number,
                retailer=retailer_obj,
                discount=form.cleaned_data['discount']
            )

            invoice_total = Decimal('0.00')
            invoice_profit = Decimal('0.00')
            total_items = 0
            product_entries = []
            
            for product_id, quantity in zip(product_ids, quantities):
                if product_id.strip() and quantity.strip():
                    product_obj = get_object_or_404(Inventory, id=product_id, user=request.user)
                    try:
                        quantity_val = int(quantity)
                        if quantity_val <= 0:
                            continue
                    except ValueError:
                        continue

                    cost_price = Decimal(product_obj.sale_price)  
                    gst = Decimal(product_obj.gst)
                    profit = Decimal(product_obj.profit)
                    
                    # Calculate total amount including GST
                    total_amount = (cost_price * quantity_val) * (1 + (gst / Decimal(100)))
                    total_profit = (profit * quantity_val)
                    
                    product_entries.append(
                        ProductEntry(
                            invoice=invoice,
                            product_name=product_obj.product_name,
                            quantity=quantity_val,
                            amount=total_amount
                        )
                    )
                    
                    product_obj.quantity -= quantity_val
                    product_obj.save()
                    
                    invoice_total += total_amount
                    total_items += quantity_val
                    invoice_profit += total_profit

            discount_percent = Decimal(form.cleaned_data['discount'])
            final_total = invoice_total * (1 - discount_percent / Decimal(100))
            
            # Bulk insert product entries for performance
            ProductEntry.objects.bulk_create(product_entries)
            
            if invoice.retailer:
                invoice.retailer.credit += float(final_total)
                invoice.retailer.total_sales += float(final_total)
                invoice.retailer.save()

            invoice.profit = invoice_profit
            invoice.save()
            
            message = "Invoice added successfully!"
            return redirect('out_invoice_list')
        else:
            print("Form errors:", form.errors)
    else:
        form = OutwardInvoiceForm()

    profile = get_object_or_404(Profile, user=request.user)
    firmname = profile.firm_name

    return render(request, "outward_supply/add_outward_invoice.html", {
        "form": form,
        "retailers": retailers,
        "productJSON": productJSON,
        "message": message,
        "firmname": firmname
    })



@login_required
def out_invoice_list(request):
    query = request.GET.get('query', '')
    invoices = Outward_Invoice.objects.filter(user=request.user)
    
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
    
    return render(request, "outward_supply/outward_invoice_list.html", {"invoices": invoices})

@login_required
def out_invoice_detail(request, bill_number):
    invoice = get_object_or_404(Outward_Invoice, bill_number=bill_number, user=request.user)
    return render(request, "outward_supply/out_invoice_detail.html", {"invoice": invoice})

@login_required
def delete_retailer(request, id):
    ret = get_object_or_404(Retailer, id=id, user=request.user)
    ret.delete()
    return redirect('view_retailers')

@login_required
def bulk_delete_retailers(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_retailers')
        Retailer.objects.filter(id__in=selected_ids).delete()
    return redirect('view_retailers')

