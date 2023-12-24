from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ContactUs, Cart
from products.models import Products 
 

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
    
    messages.success(request, "Product added to cart ") 
    return redirect('/user_home')