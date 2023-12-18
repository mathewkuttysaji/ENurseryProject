from typing import Any
from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomerCreationForm(UserCreationForm):
    name : forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone : forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    email : forms.CharField(max_length=254, widget=forms.EmailInput(attrs={'class':'form-control'}))
    
    class Meta:

        model = get_user_model()

        fields = (
            'name', 'phone', 'email', 'password1', 'password2'
        )

    def __init__(self, *args,**kwargs):
        super(CustomerCreationForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'