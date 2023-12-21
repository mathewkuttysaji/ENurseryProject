from django.shortcuts import render
from .forms import ProductUploadForms 
from django.contrib import messages
from django.shortcuts import get_object_or_404 
from .models import Products
# Create your views here.

def product_upload(request):

    if request.method == 'POST':
        form = ProductUploadForms(request.POST, request.FILES) 
        print("form valid", form.is_valid())
        if form.is_valid():
            product = form.save()  
            messages.success(request, "New product uploaded !!!")
            return render(request, 'products/product_upload.html')
        else:
            messages.error(request, "Failed to upload new product !!!")
            return render(request, 'products/product_upload.html')
    else:
        form = ProductUploadForms()
    return render(request, 'products/product_upload.html', {'form' : form}) 


def update_product(request):
    
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Products, id = product_id) 

    if request.method == 'POST':
        form = ProductUploadForms(request.POST, request.FILES, instance = product) 

        if form.is_valid():
            updated_data = {field : form.cleaned_data[field] for field in form.cleaned_data if form.cleaned_data[field] is not None} 

            for field, value in updated_data.items():
                setattr(product, field, value) 

            product.save()

            messages.success(request, "Product uploaded successfully !!!") 
            return render(request, "products/product_update.html", {'form' : form, 'product' : product}) 
        else:
            messages.error(request, "Product uploaded failed !!! Please try again") 
            return render(request, "products/product_update.html", {'form' : form, 'product' : product})
    else:
        form = ProductUploadForms(instance = product)
        return render(request, "products/product_update.html", {'form' : form, 'product' : product})
