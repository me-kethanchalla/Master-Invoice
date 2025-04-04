from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
# Create your views here.
from inward_supply.models import Supplier
from outward_supply.models import Retailer
from outward_supply.models import Outward_Invoice, ProductEntry
from transactions.models import Transaction
from django.db.models import Sum, Avg, Max, Count
import datetime


'''
TODOS:

'''



def AddMonths(d,x):
    newmonth = (((d.month - 1)+x )%12 ) + 1
    newyear  = int(d.year+((( d.month-1)+x )/12 ))
    if newmonth == 2 and d.day > 28:
        return datetime.date( newyear, newmonth, 28)
    try :
        return datetime.date( newyear, newmonth, d.day)
    except Exception as e:
        print(e)
        return datetime.date( newyear, newmonth, d.day - 1)

def view(request):
    if request.user.is_anonymous:
        return HttpResponseForbidden("You must be logged in to access this page.")
    
    
    print(request.user)
    today_date = datetime.date.today()
    one_month_back_date = AddMonths(today_date, -1)
    three_month_back_date = AddMonths(today_date, -3)
    six_month_back_date = AddMonths(today_date, -6)
    
    # db query for tables
    # 1 month
    one_month_queryset = ProductEntry.objects.filter(invoice__user=request.user,
                                                     invoice__date__range=[one_month_back_date, today_date])\
        .values('product_name')\
        .annotate(product_sales=Sum('quantity'),
                  average_sales=Avg('quantity'),
                  net_profit=Sum('amount'))\
        .order_by('-product_sales')[:5]
    # 3 months
    three_month_queryset = ProductEntry.objects.filter(invoice__user=request.user,
                                                       invoice__date__range=[three_month_back_date, today_date])\
        .values('product_name')\
        .annotate(product_sales=Sum('quantity'),
                  average_sales=Avg('quantity'),
                  net_profit=Sum('amount'))\
        .order_by('-product_sales')[:5]
    # 6 months
    six_month_queryset = ProductEntry.objects.filter(invoice__user=request.user,
                                                     invoice__date__range=[six_month_back_date, today_date])\
        .values('product_name')\
        .annotate(product_sales=Sum('quantity'),
                  average_sales=Avg('quantity'),
                  net_profit=Sum('amount'))\
        .order_by('-product_sales')[:5]
    
    # total number of suppliers
    total_num_suppliers = Supplier.objects.filter(user=request.user).count()
    
    # total number of retailers
    total_num_retailers = Retailer.objects.filter(user=request.user).count()
    
    
    # converting queryset to list
    one_month = [{'product_name': p['product_name'], 
              'product_sales': p['product_sales'], 
              'average_sales': round(p['average_sales'], 2), 'net_profit': round(p['net_profit'], 2)} 
              for p in one_month_queryset]
    three_month = [{'product_name': p['product_name'], 'product_sales':p['product_sales'], 'average_sales': round(p['average_sales'], 2), 'net_profit': round(p['net_profit'], 2)}    for p in three_month_queryset]
    six_month = [{'product_name': p['product_name'], 'product_sales':p['product_sales'], 'average_sales': round(p['average_sales'], 2), 'net_profit': round(p['net_profit'], 2)}    for p in six_month_queryset]
    
    print(one_month)
    
    return render(request, 'analysis/graph.html',  {
        'total_num_suppliers': total_num_suppliers,
        'total_num_retailers': total_num_retailers,
        'one_month_sales': one_month,
        'three_month_sales': three_month,
        'six_month_sales': six_month
    })


def get_top_suppliers(request):
    
    suppliers = Supplier.objects.filter(user=request.user).order_by("-total_sales")[:5]
    
    suppliers_names = []
    suppliers_total_sales = []
    
    suppliers_names = [supplier.person_name for supplier in suppliers]
    suppliers_total_sales = [supplier.total_sales for supplier in suppliers]
    
        
    return JsonResponse({"suppliers_name": suppliers_names,
                         "suppliers_total_sales": suppliers_total_sales})
    

def get_top_retailers(request):
    
    
    retailers  = Retailer.objects.filter(user=request.user).order_by("-total_sales")[:5]
    
    retailers_names = []
    retailers_total_sales = []
    
    retailers_names = [retailer.person_name for retailer in retailers]
    retailers_total_sales = [retailer.total_sales for retailer in retailers]
    
        
    return JsonResponse({"retailers_name": retailers_names,
                         "retailers_total_sales": retailers_total_sales})
    

def get_profit(request):
    
    
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    if not from_date or not to_date:
        return HttpResponseForbidden("Both from_date and to_date must be provided.")
    
    # Ensure that from_date is less than to_date
    if from_date > to_date:
        return HttpResponseForbidden("From date must be less than to date.")
    
    # Extraction of Query set
    profits_query_set = Outward_Invoice.objects.filter(
        user=request.user,
    date__range=[from_date, to_date]
).values(
    'date'
).annotate(
    total_profit_sum = Sum('profit'), # annotate the profit values
).order_by('date')
    
    if not profits_query_set:
        return JsonResponse({"message": "No data found for the given date range.",
                             "total_profits": round(0, 2),
                             "percentage_increment": round(0, 2),
                              "avg_profits": round(0, 2),
                        "max_profits": round(0, 2),
                             })
    last_date = profits_query_set.last()
    first_date = profits_query_set.first()
    
    # try if the percentage increment is valid else set the element to 0
    try: 
        if last_date['total_profit_sum'] != first_date['total_profit_sum']:
            percentage_increment = (last_date['total_profit_sum']-max(first_date['total_profit_sum'], 0.5))/max(first_date['total_profit_sum'], 0.5) * 100
        else : percentage_increment = 0.00
    except Exception as e:
        print('Exception: ', e)
    
    
    # Query Average and Maximum in Query set
    avg_profits = profits_query_set.aggregate(Avg('total_profit_sum'))
    max_profits = profits_query_set.aggregate(Max('total_profit_sum'))
    total_profits = profits_query_set.aggregate(Sum('total_profit_sum'))
    
    # If the respective annotate is None it returns 0
    avg_profit_value = avg_profits.get('total_profit_sum__avg', 0)
    max_profit_value = max_profits.get('total_profit_sum__max', 0)
    total_profit_value = total_profits.get('total_profit_sum__sum', 0)
    # Return the response
    return JsonResponse(
        {"profits": [(profit['total_profit_sum']) for profit in profits_query_set],
         "dates": [(profit['date']) for profit in profits_query_set],
         "avg_profits": round(avg_profit_value, 2),
         "max_profits": round(max_profit_value, 2),
          "total_profits": round(total_profit_value, 2),
          "percentage_increment": round(percentage_increment, 2)
          }
    )
    

def get_sales(request):
    
    # Get the date range
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    if not from_date or not to_date:
        return HttpResponseForbidden("Both from_date and to_date must be provided.")
    
    # Ensure that from_date is less than to_date
    if from_date > to_date:
        return HttpResponseForbidden("From date must be less than to date.")
    
    # Extraction of Query set
    sales_query_set = ProductEntry.objects.filter(  invoice__user=request.user,
    invoice__date__range=[from_date, to_date])\
        .values('invoice__date')\
        .annotate(
            total_sales=Sum('quantity'),  # Total quantity sold on that date
            total_amount=Sum('amount')  # Total sale for that date
        ).order_by('invoice__date')  # Order by date

    # If no data is found
    if not sales_query_set:
        return JsonResponse({"message": "No data found for the given date range.",
                             "total_sales": round(0, 2),
                             "percentage_increment": round(0, 2),
                              "avg_sales": round(0, 2),
                        "max_sales": round(0, 2),
                             })
    
    # Convert to list
    sales_by_date = []
    for sale in sales_query_set:
        sales_by_date.append({
            'date': sale['invoice__date'],
            'total_amount': sale['total_amount'],
            'total_sales': sale['total_sales'],
        })

    
    last_date = sales_query_set.last()
    first_date = sales_query_set.first()
    try: 
        if last_date['total_sales'] != first_date['total_sales']:
            percentage_increment = (last_date['total_sales']-max(first_date['total_sales'], 0.5))/max(first_date['total_sales'], 0.5) * 100
        else : percentage_increment = 0.00
    except Exception as e:
        print('Exception: ', e)
    
    avg_sales = sales_query_set.aggregate(Avg('total_sales'))
    max_sales = sales_query_set.aggregate(Max('total_sales'))
    total_sales = sales_query_set.aggregate(Sum('total_sales'))
    
    avg_sales_value = avg_sales.get('total_sales__avg', 0)
    max_sales_value = max_sales.get('total_sales__max', 0)
    total_sales_value = total_sales.get('total_sales__sum', 0)
    return JsonResponse(
        {"sales": [(sale['total_sales']) for sale in sales_by_date],
         "dates": [(sale['date']) for sale in sales_by_date],
         "avg_sales": round(avg_sales_value, 2),
         "max_sales": round(max_sales_value, 2),
         "total_sales": round(total_sales_value, 2),
         "percentage_increment": round(percentage_increment, 2)
         }
    )


def allsales(request):
    
     
    print(request.user)
    today_date = datetime.date.today()
    one_month_back_date = AddMonths(today_date, -1)
    three_month_back_date = AddMonths(today_date, -3)
    six_month_back_date = AddMonths(today_date, -6)
    
    # db query for tables
    # 1 month
    one_month_queryset = ProductEntry.objects.filter(invoice__user=request.user,
                                                     invoice__date__range=[one_month_back_date, today_date])\
        .values('product_name')\
        .annotate(product_sales=Sum('quantity'),
                  average_sales=Avg('quantity'),
                  net_profit=Sum('amount'))\
        .order_by('-product_sales')
    # 3 months
    three_month_queryset = ProductEntry.objects.filter(invoice__user=request.user,
                                                       invoice__date__range=[three_month_back_date, today_date])\
        .values('product_name')\
        .annotate(product_sales=Sum('quantity'),
                  average_sales=Avg('quantity'),
                  net_profit=Sum('amount'))\
        .order_by('-product_sales')
    # 6 months
    six_month_queryset = ProductEntry.objects.filter(invoice__user=request.user,
                                                     invoice__date__range=[six_month_back_date, today_date])\
        .values('product_name')\
        .annotate(product_sales=Sum('quantity'),
                  average_sales=Avg('quantity'),
                  net_profit=Sum('amount'))\
        .order_by('-product_sales')
    

    
    
    # converting queryset to list
    one_month = [{'product_name': p['product_name'], 
              'product_sales': p['product_sales'], 
              'average_sales': round(p['average_sales'], 2), 'net_profit': round(p['net_profit'], 2)} 
              for p in one_month_queryset]
    three_month = [{'product_name': p['product_name'], 'product_sales':p['product_sales'], 'average_sales': round(p['average_sales'], 2), 'net_profit': round(p['net_profit'], 2)}    for p in three_month_queryset]
    six_month = [{'product_name': p['product_name'], 'product_sales':p['product_sales'], 'average_sales': round(p['average_sales'], 2), 'net_profit': round(p['net_profit'], 2)}    for p in six_month_queryset]
    
    
    return render(request, 'analysis/allsales.html', {
        'one_month_sales': one_month,
        'three_month_sales': three_month,
        'six_month_sales': six_month
    })
    
    
def outward_invoice_bill(request):
    today_date = datetime.date.today()
    one_year_date = AddMonths(today_date, -2)
    try: 
        outward_invoice_bill_query_set = Outward_Invoice.objects\
            .filter(user=request.user, date__range=[one_year_date, today_date]).values('date')\
            .annotate(bill_count=Count('bill_number'))
        dates = [entry['date']  for entry in outward_invoice_bill_query_set]
        bill_count = [entry['bill_count'] for entry in outward_invoice_bill_query_set]
        return JsonResponse({
        "bill_count": bill_count,
        "dates": dates,
        "total_num_bills": len(bill_count)
    })
    except Exception as e:
        print(e)
        return JsonResponse({
            "bill_count": [],
            "dates": [],
             "total_num_bills": 0
        })
        
        
        
def inward_transaction(request):
    
    today_date = datetime.date.today()
    one_year_date = AddMonths(today_date, -2)
    try: 
        inward_transaction_query_set = Transaction.objects\
            .filter(user=request.user, add_date__range=[one_year_date, today_date], type=0).values('add_date')\
            .annotate(payment=Sum('payment'))\
            .order_by('add_date')
        dates = [entry['add_date']  for entry in inward_transaction_query_set]
        payments = [entry['payment'] for entry in inward_transaction_query_set]
        total_payments = sum(payments)
        return JsonResponse({
        "payments": payments,
        "dates": dates,
        "total_payments": total_payments
    })
    except Exception as e:
        print("hello")
        print(e)
        return JsonResponse({
            "payments": [],
            "dates": [],
             "total_payments": 0
        })
    pass