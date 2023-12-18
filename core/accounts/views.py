from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomerCreationForm
from django.urls import reverse
from django.contrib import messages


# Create your views here.

def index_view(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'registration/login.html')
    else:
        form = CustomerCreationForm()
    return render(request, "registration/register.html", {'form':form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password') 

        customer = authenticate(request, email=email, password=password) 
        
        if customer is not None:
            login(request, customer)

            if customer.is_superuser:
                return redirect('/admin')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid credentials. Please try again. If you are new please login")
    else: 
        return render(request, 'registration/login.html')
    
def home(request):
    return render(request, "home.html")