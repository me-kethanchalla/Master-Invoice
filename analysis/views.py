from re import S
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
# Create your views here.
from inward_supply.models import Supplier
from outward_supply.models import Retailer
# from outward_supply.models import outwardInvoiceBill
from django.db.models import Sum, Avg

def view(request):
    if request.user.is_anonymous:
        return HttpResponseForbidden("You must be logged in to access this page.")
    
    total_num_suppliers = Supplier.objects.filter(user=request.user).count()
    total_num_retailers = Retailer.objects.filter(user=request.user).count()
    return render(request, 'analysis/graph.html', {
        'total_num_suppliers': total_num_suppliers,
        'total_num_retailers': total_num_retailers,
    })


def get_top_suppliers(request):
    '''
    TODOS: 
    
    '''
    
    suppliers = Supplier.objects.filter(user=request.user).order_by("-total_sales")[:5]
    
    suppliers_names = []
    suppliers_total_sales = []
    
    suppliers_names = [supplier.person_name for supplier in suppliers]
    suppliers_total_sales = [supplier.total_sales for supplier in suppliers]
    
        
    return JsonResponse({"suppliers_name": suppliers_names,
                         "suppliers_total_sales": suppliers_total_sales})
    

def get_top_retailers(request):
    '''
    TODOS: 
    
    '''
    
    retailers  = Retailer.objects.filter(user=request.user).order_by("-total_sales")[:5]
    
    retailers_names = []
    retailers_total_sales = []
    
    retailers_names = [retailer.person_name for retailer in retailers]
    retailers_total_sales = [retailer.total_sales for retailer in retailers]
    
        
    return JsonResponse({"retailers_name": retailers_names,
                         "retailers_total_sales": retailers_total_sales})
    
    

# def get_profit(request):
    
#     '''
#     TODOS: 
#     1. extract profit on one month basis
#     2. route to the graph
#     '''
    
    
#     profits_query_set = outwardInvoiceBill.objects.filter(
#         date__range=[request.from_date, request.to_date]
#         ).values(
#             'date'
#             ).annotate(
#                 total_profit_sum = Sum('total_profit')
#                 ).order_by('date')
    
#     return JsonResponse(
#         profits_query_set
#     )
    

# def get_sales():
#     '''
#     TODOS:
#     1. extract sales on one month basis
#     2. route to the graph
#     '''
    
    
    
    
#     pass

def allsales(request):
    return render(request, 'analysis/allsales.html')