from django.shortcuts import render, get_object_or_404
from accounts.models import Customers 
from products.models import Products, Purchase, PurchaseItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 

# Create your views here.

def view_users(request):
    customers_list = Customers.objects.all().order_by('id')
    paginator = Paginator(customers_list, 10) 

    page = request.GET.get('page')
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    return render(request, "admin/view_users.html", {'customers': customers}) 


def view_products(request):
    product_list = Products.objects.all().order_by('product_name') 
    paginator = Paginator(product_list, 10) 

    page = request.GET.get('page') 

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, "admin/view_products.html", {'products' : products}) 


def view_purchases(request):
    purchases = Purchase.objects.all()
    
    purchase_info_list = []

    for purchase in purchases:
        purchase_items = purchase.purchaseitem_set.all()
        total_price = sum(item.unit_price for item in purchase_items)
        
        purchase_info_list.append({ 
            'purchase_id': purchase.id,
            'user': purchase.customer,
            'total_price': total_price,
            'products': [item.product for item in purchase_items],
            'purchase_date': purchase.purchase_date,

        })

    paginator = Paginator(purchase_info_list, 10)  # Show 10 purchases per page
    page = request.GET.get('page')

    try:
        purchase_info_list = paginator.page(page)
    except PageNotAnInteger:
        purchase_info_list = paginator.page(1)
    except EmptyPage:
        purchase_info_list = paginator.page(paginator.num_pages)

    context = {
        'purchase_info_list': purchase_info_list,
        'paginator': paginator,
    }

    print(purchase.id, type(purchase.id))
    return render(request, 'admin/view_purchases.html', context)

def purchase_details(request):
    purchase_id = request.GET.get('purchase_id') 
    purchase = get_object_or_404(Purchase, id = purchase_id) 
    purchase_items = purchase.purchaseitem_set.all() 

    context = {
        'purchase' : purchase, 
        'purchase_items' : purchase_items
    } 

    return render(request, 'admin/details_purchase.html', context)