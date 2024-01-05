from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ContactUs, Cart
from products.models import Products, Purchase, PurchaseItem  
from django.http import JsonResponse 
from .forms import PurchaseForm 
from django.db import transaction 

# Create your views here.

def user_home(request): 
    products = Products.objects.filter(product_quantity__gt = 0).order_by('product_name')
    return render(request, "home.html", {'products' : products})

def search_view(request):
    term = request.POST.get('h_search') 

    if term:
        products = Products.objects.filter(product_name__icontains = term)
        if products: 
            context = { 
                'term' : term, 'products' : products, 
            } 
            return render(request, 'home.html', context) 
        else:
            messages.error(request, 'Sorry.There is no such products')  
            return redirect('/user_home')

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
                return redirect('/user_home')
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
    
    return redirect('/user_home')  


def get_cart_items(user):
    return Cart.objects.filter(user=user) 

def clear_cart(user):
    Cart.objects.filter(user=user).delete()

def view_cart(request): 
    user = request.user 
    form = PurchaseForm()
    cart_products = get_cart_items(user) 
    return render (request, "users/view_cart.html", {'cart_products' : cart_products, 'form' : form}) 

def remove_from_cart(request):
    cart_id = request.GET.get('cart_id') 
    cart_item = get_object_or_404(Cart, id=cart_id) 
    cart_item.delete()
    return redirect('/view_cart')     


def update_cart_quantity(request, product_id, quantity):
    cart_item = get_object_or_404(Cart, id=product_id)  
    cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({'status': 'success'})

# ... your other imports ...

def make_purchase(request):
    user = request.user
    purchases = Purchase.objects.filter(customer=user)

    # Check if the user has any purchases
    if purchases.exists():
        # Accessing related PurchaseItem instances for each Purchase
        purchase_items_list = []
        for purchase in purchases:
            purchase_items = purchase.purchaseitem_set.all()
            purchase_items_list.append({
                'purchase': purchase,
                'purchase_items': purchase_items,
            })

        context = {
            'purchase_items_list': purchase_items_list,
        }
        
        return render(request, 'users/make_purchase.html', context)
    else:
        return render(request, 'users/make_purchase.html')
        



def purchase_next(request):

    if request.method == 'POST':
        form = PurchaseForm(request.POST) 

        print("Form validity", form.is_valid())
        if form.is_valid():

            user = request.user
            purchase = Purchase(
                customer = user, 
                address = form.cleaned_data['address'], 
                total_amount = 0
            ) 
            purchase.save() 

            cart_products = Cart.objects.filter(user = user) 

            for cart_product in cart_products:
                quantity = cart_product.quantity 
                unit_price = (cart_product.product.product_price * quantity) 
                
                print(f'{cart_product.product.product_name} price = {unit_price}')  

                purchase_item = PurchaseItem(
                    purchase = purchase, 
                    product = cart_product.product, 
                    quantity = quantity, 
                    unit_price = unit_price
                ) 

                purchase_item.save() 

            purchase.total_amount = sum( 
                 item.unit_price for item in purchase.purchaseitem_set.filter(purchase=purchase)
            ) 
            
            purchase.save() 
        else:
            messages.error(request, "Something went wrong. Please try again later")
        Cart.objects.filter(user = user).delete() 

        for purchase_item in purchase.purchaseitem_set.all():
                product = purchase_item.product
                remaining_quantity = product.product_quantity - purchase_item.quantity
                product.product_quantity = remaining_quantity
                product.save()

        return redirect('make_purchase')
    else:
        form = PurchaseForm() 

    return render(request, "users/address.html", {'form' : form}) 
 

def cancel_purchase(request):
    purchase_id = request.GET.get('purchase_id') 
    purchase = get_object_or_404(Purchase, id = purchase_id) 
    purchase.delete()
    return redirect('/make_purchase')

