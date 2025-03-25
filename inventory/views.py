from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Inventory
from django.db.models import Q
from .forms import InventoryForm

@login_required
def inventory_list(request):
    query = request.GET.get('query', '')
    if query:
        inventory = Inventory.objects.filter(
            (Q(product_name__icontains=query) | Q(item_id__icontains=query)),
            user=request.user
        )
    else:
        inventory = Inventory.objects.filter(user=request.user)
    
    return render(request, 'inventory/inventory.html', {'inventory': inventory})

    # inventory = Inventory.objects.filter(user=request.user)
    # return render(request, 'inventory/inventory.html', {'inventory': inventory})

@login_required
def add_inventory(request):
    message = ""
    message_type = ""
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory_item = form.save(commit=False)
            inventory_item.user = request.user
            inventory_item.profit = inventory_item.sale_price - inventory_item.cost_price
            
            if Inventory.objects.filter(user=request.user, item_id=inventory_item.item_id).exists():
                message = "Inventory item with this Item ID already exists for your account."
                message_type = "error"
            else:
                inventory_item.total_qty_sold = 0
                inventory_item.save()
                message = "Inventory item added successfully!"
                message_type = "success"
                form = InventoryForm()
        else:
            print("Form errors:", form.errors)
    else:
        form = InventoryForm()
    return render(request, 'inventory/add_inventory.html', {'form': form, 'message': message,  'message_type': message_type})

@login_required
def edit_inventory(request, id):
    item = get_object_or_404(Inventory, id=id, user=request.user)
    message = ""
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            updated_item = form.save(commit=False)
            updated_item.profit = updated_item.sale_price - updated_item.cost_price
            updated_item.save()
            message = "Inventory item updated successfully!"
            return redirect('inventory_list')
    else:
        form = InventoryForm(instance=item)
    return render(request, 'inventory/edit_inventory.html', {'form': form, 'message': message, 'item': item})

@login_required
def delete_inventory(request, id):
    item = get_object_or_404(Inventory, id=id, user=request.user)
    item.delete()
    return redirect('inventory_list')
