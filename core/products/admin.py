from django.contrib import admin
from .models import Products, Purchase, PurchaseItem

# Register your models here.

admin.site.register(Products) 
admin.site.register(Purchase) 
admin.site.register(PurchaseItem)