from django.shortcuts import render
from .forms import ProductUploadForms 
from django.contrib import messages

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