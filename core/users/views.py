from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ContactUs, Cart
from products.models import Products  
from .forms import PurchaseForm 
from products.models import Purchase, PurchaseItem 
from django.http import JsonResponse
 

# Create your views here.

def user_home(request): 
    products = Products.objects.filter(product_quantity__gt = 0).order_by('product_name')
    return render(request, "home.html", {'products' : products})


def contact_us_view(request):
    if request.method == 'POST':
        message = request.POST.get('message') 
        user_instance = request.user

        if message:
            contact_us = ContactUs.objects.create(
                customer = user_instance, message_text = message
            )
            if contact_us: 
                contact_us.save()
                return render(request, "home.html")
        pass
    return render(request, "users/contactus.html")

def add_to_cart(request): 

    product_id = request.GET.get('product_id')
    product = get_object_or_404(Products, id=product_id) 

    cart_item, created = Cart.objects.get_or_create(
        user = request.user, 
        product = product
    ) 

    if not created:
        cart_item.quantity += 1
        cart_item.save() 
    
    messages.success(request, "Product added to cart ", extra_tags="added_to_cart") 
    return redirect('/user_home')  


def get_cart_items(user):
    return Cart.objects.filter(user=user) 

def clear_cart(user):
    Cart.objects.filter(user=user).delete()

def view_cart(request): 
    user = request.user
    cart_products = get_cart_items(user)
    return render (request, "users/view_cart.html", {'cart_products' : cart_products}) 

def remove_from_cart(request):
    cart_id = request.GET.get('cart_id') 
    cart_item = get_object_or_404(Cart, id=cart_id) 
    cart_item.delete()
    return redirect('/view_cart')     

def make_purchase(request): 
    if request.method == 'POST':

        form = PurchaseForm(request.POST) 
        print(form) 
        print("form validity", form.is_valid()) 
        if form.is_valid():
            try: 
                user = request.user 
                purchase = Purchase.objects.create(customer = user) 

                cart_items = get_cart_items(user) 

                if cart_items:
                    for cart_item in cart_items:
                        PurchaseItem.objects.create( 
                            purchase = purchase, 
                            product = cart_item.product, 
                            quantity = cart_item.quantity 
                        ) 

                        clear_cart(user) 

                        return redirect('\thankyou') 
                else:
                    return render('\purchase')
            except ValidationError as e:
                return redirect('Purchasefailed') 
    else:
        return render(request, "users/make_purchase.html") 

def update_cart_quantity(request, product_id, quantity):
    cart_item = get_object_or_404(Cart, id=product_id)  
    cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({'status': 'success'})
