from django.shortcuts import render 
from accounts.models import Customers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def admin_home(request):
    return render(request, "admin/admin_home.html")

def view_users(request):
    customers_list = Customers.objects.all().order_by('id')
    paginator = Paginator(customers_list, 10)  # Show 10 customers per page

    page = request.GET.get('page')
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    return render(request, "admin/view_users.html", {'customers': customers})
