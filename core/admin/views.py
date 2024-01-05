from django.shortcuts import render, get_object_or_404
from accounts.models import Customers 
from products.models import Products, Purchase, PurchaseItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from users.models import ContactUs
from django.core.mail import send_mail 
from django.conf import settings
from django.contrib import messages
# Create your views here.

def view_users(request):
    customers_list = Customers.objects.filter(is_superuser = False).order_by('id')
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

def view_messages(request):
    messages = ContactUs.objects.all().order_by('id')
    messages_per_page = 10
    paginator = Paginator(messages, messages_per_page) 
    page = request.GET.get('page') 

    try:
        messages = paginator.page(page) 
    except PageNotAnInteger:
        messages = paginator.page(1) 
    except EmptyPage:
        messages = paginator.page(1) 
    return render(request, 'admin/view_messages.html', {'messages' : messages}) 

def reply_message(request): 
    if request.method == 'POST': 

        print(request.POST)
        message = request.POST.get('reply_message') 
        subject = 'Reply from E-Nursery team' 
        recipient_email = request.POST.get('recipient_address')
        recipient_list = [recipient_email] 
        from_email = settings.EMAIL_HOST_USER

        print(recipient_email) 
        print(f'subject {subject}, message {message}, to {recipient_list}, from {from_email}') 

        try:
            send_mail(subject, message, from_email, recipient_list) 
            messages.success(request, "Replay sent successfully !!!")
        except Exception as e:
            messages.error(request, 'Error occured. Please try again later !!!') 
        
        return render(request, 'admin/reply_message.html')
    else:
        message_id = request.GET.get('message_id') 
        message = ContactUs.objects.get(id = message_id) 
        return render(request, "admin/reply_message.html", {'message' : message}) 
