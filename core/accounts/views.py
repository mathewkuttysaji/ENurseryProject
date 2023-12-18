from django.shortcuts import render
from .forms import CustomerCreationForm

# Create your views here.

def index_view(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html')
    else:
        form = CustomerCreationForm()
    return render(request, "registration/register.html", {'form':form})