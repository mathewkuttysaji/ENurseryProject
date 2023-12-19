from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactUs

# Create your views here.

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
