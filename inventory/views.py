# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventory
from django.contrib.auth.models import User

# View to display the list of inventory items
def inventory_list(request):
    # Fetch all inventory items
    inventory = Inventory.objects.filter(user=request.user)
    return render(request, 'inventory/inventory.html', {'inventory': inventory})

# View to add a new inventory item
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Inventory

@login_required  # Ensure the user is logged in
def add_inventory(request):
    if request.method == 'POST':
        # Get the form data
        product_name = request.POST['product_name']
        item_id = request.POST['item_id']
        quantity = int(request.POST['quantity'])  # Convert to int
        cost_price = float(request.POST['cost_price'])  # Convert to float
        sale_price = float(request.POST['sale_price'])  # Convert to float
        max_retail_price = float(request.POST['max_retail_price'])  # Convert to float
        gst = float(request.POST['gst'])  # Convert to float

        # Calculate the profit
        profit = sale_price - cost_price  # Ensure cost_price and sale_price are floats

        # Create the new inventory item
        new_inventory_item = Inventory(
            user=request.user,  # Assign the logged-in user to this inventory
            product_name=product_name,
            item_id=item_id,
            quantity=quantity,
            cost_price=cost_price,
            sale_price=sale_price,
            max_retail_price=max_retail_price,
            gst=gst,
            profit=profit,
            total_qty_sold=0  # Initialize with 0 or based on your requirement
        )
        
        new_inventory_item.save()

        return redirect('inventory_list')  # Redirect to the inventory list page
    return render(request, 'inventory/add_inventory.html')

# View to edit an existing inventory item
def edit_inventory(request, id):
    # Fetch the inventory item by ID
    item = get_object_or_404(Inventory, id=id, user=request.user)

    if request.method == 'POST':
        # Update the item with the data from the POST request
        item.product_name = request.POST['product_name']
        item.item_id = request.POST['item_id']
        item.quantity = request.POST['quantity']
        item.cost_price = request.POST['cost_price']
        item.sale_price = request.POST['sale_price']
        item.max_retail_price = request.POST['max_retail_price']
        item.gst = request.POST['gst']

        # Recalculate profit
        item.profit = str(float(item.sale_price) - float( item.cost_price))
        item.save()  # Save the updated item

        return redirect('inventory_list')  # Redirect to the inventory list after saving

    # If not a POST request, render the edit form
    return render(request, 'inventory/edit_inventory.html', {'item': item})

# View to delete an inventory item
@login_required
def delete_inventory(request, id):
    item = get_object_or_404(Inventory, id=id, user=request.user)  # Ensure user owns this item
    item.delete()
    return redirect('inventory_list')

