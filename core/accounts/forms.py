from collections.abc import Mapping
from typing import Any
from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm

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

class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'phone'] 

    def __init__(self, *args, **kwargs):
        super(ChangeProfileForm, self).__init__(*args, **kwargs) 

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'

class StyledPasswordForm(PasswordChangeForm):

    def __init__(self,  *args, **kwargs):
        super(StyledPasswordForm, self).__init__(*args, **kwargs) 

        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'



class StyledPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'}) 


