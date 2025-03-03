from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RetailerForm
from .models import Retailer

@login_required
def add_retailer(request):
    message = ""
    if request.method == 'POST':
        form = RetailerForm(request.POST)
        if form.is_valid():
            retailer = form.save(commit=False)
            retailer.user = request.user
            retailer.save()
            message = "Retailer added successfully!"
            # Reset the form by creating a new instance
            form = RetailerForm()
    else:
        form = RetailerForm()
    return render(request, 'outward_supply/add_retailer.html', {'form': form, 'message': message})

def view_retailers(request):
    retailers = Retailer.objects.all()
    return render(request, 'outward_supply/view_retailers.html', {'retailers': retailers})
