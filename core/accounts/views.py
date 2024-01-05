from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomerCreationForm, ChangeProfileForm, StyledPasswordForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from products.models import Products


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
                
                return redirect('/user_home')
        else:
            messages.error(request, "Invalid credentials. Please try again. If you are new please login")
    else: 
        return render(request, 'registration/login.html')
    return render(request, 'registration/login.html') 
    

def logout_view(request):
    logout(request)

    return redirect(reverse('index'))


def edit_profile_view(request):
    user = request.user

    if request.method == 'POST':
        user_form = ChangeProfileForm(request.POST, instance=user)
        password_form = StyledPasswordForm(user, request.POST)

        print(user_form.is_valid(), "user form valid")
        print(password_form.is_valid(), "password form valid")
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            messages.success(request, 'Profile updated successfully.')
            return render(request, 'registration/change_user_details.html')
    else:
        user_form = ChangeProfileForm(instance=user)
        password_form = StyledPasswordForm(user)

    return render(request, 'registration/change_user_details.html', {'user_form': user_form, 'password_form': password_form})
