from django.shortcuts import render 
from accounts.models import Customers 
from products.models import Products
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def admin_home(request):
    return render(request, "admin/admin_home.html")

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


