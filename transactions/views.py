from django.shortcuts import render, get_object_or_404, redirect
from inventory.models import Inventory
from inward_supply.models import Supplier
from outward_supply.models import Retailer
from .models import Transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def pending(request):
 suppliers = Supplier.objects.all()
 retailers = Retailer.objects.all()
 return render(request, 'transactions/pending.html', {'suppliers': suppliers, 'retailers': retailers})

def view_transaction_history(request):
 suppliers = Supplier.objects.all()
 retailers = Retailer.objects.all()
 transactions = Transaction.objects.all()
 return render(request, 'transactions/view_transaction_history.html', {'suppliers': suppliers, 'retailers': retailers, 'transactions': transactions})

def add_outward_transaction(request):
 retailers = Retailer.objects.all()
 return render(request, 'transactions/add_outward_transaction.html',{'retailers': retailers})
def add_inward_transaction(request):
 suppliers = Supplier.objects.all()
 return render(request, 'transactions/add_inward_transaction.html', {'suppliers': suppliers})

@login_required
def update_transaction_supplier(request):
    suppliers = Supplier.objects.all()
    retailers = Retailer.objects.all()
    if request.method == 'POST':
        transactions = request.POST.getlist('firm_name[]')
        amounts = request.POST.getlist('amount_paid[]')
        remarks = request.POST.getlist('remarks[]')
        # date = request.POST.get('date')
        for i in range(len(transactions)):
            firm_name = transactions[i]
            payment = float(amounts[i])
            remark = remarks[i]
            person_name = None
            for supplier in suppliers:
                if supplier.firm_name == firm_name:
                    person_name = supplier.person_name
                    supplier.debit = supplier.debit - payment
                    supplier.save()
                    break
            if not person_name:
                person_name = "Unknown"
                Transaction.objects.create(
                user=request.user,
                firm_name=firm_name,
                person_name=person_name,
                # date=date,
                payment=payment,
                remarks=remark,
                type=0
            )
            else:
               
               Transaction.objects.create(
                user=request.user,
                firm_name=firm_name,
                person_name=person_name,
                # date=date,
                payment=payment,
                remarks=remark,
                type=0
            )
        messages.success(request, "Transactions updated successfully!")
        return redirect('pending')
    return render(request, 'transactions/add_inward_transaction.html', {'suppliers': suppliers, 'retailers': retailers})


@login_required
def update_transaction_retailer(request):
    suppliers = Supplier.objects.all()
    retailers = Retailer.objects.all()
    if request.method == 'POST':
        transactions = request.POST.getlist('firm_name[]')
        amounts = request.POST.getlist('amount_paid[]')
        remarks = request.POST.getlist('remarks[]')
        # date = request.POST.get('date')
        for i in range(len(transactions)):
            firm_name = transactions[i]
            payment = float(amounts[i])
            remark = remarks[i]
            person_name = None
            for retailer in retailers:
                if retailer.firm_name == firm_name:
                    person_name = retailer.person_name
                    retailer.credit = retailer.credit - payment
                    retailer.save()
                    break
            if not person_name:
                person_name = "Unknown"
                Transaction.objects.create(
                user=request.user,
                firm_name=firm_name,
                person_name=person_name,
                # date=date,
                payment=payment,
                remarks=remark,
                type=1
            )
            else:
                Transaction.objects.create(
                user=request.user,
                firm_name=firm_name,
                person_name=person_name,
                # date=date,
                payment=payment,
                remarks=remark,
                type=1
            )
        messages.success(request, "Transactions updated successfully!")
        return redirect('pending')
    return render(request, 'transactions/pending.html', {'suppliers': suppliers, 'retailers': retailers})