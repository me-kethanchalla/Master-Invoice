from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RetailerForm
from .models import Retailer
from django.db.models import Q


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