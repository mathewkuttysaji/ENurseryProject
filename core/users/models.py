from django.core.exceptions import ValidationError
from django.db import models 
from products.models import Products 
from accounts.models import Customers
 
# Create your models here.

class ContactUs(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE) 
    date = models.DateTimeField(auto_now_add=True) 
    message_text = models.TextField()  

    def __str__(self):
        return f"{self.customer.name}'s message "
    
class Cart(models.Model):
    user = models.ForeignKey(Customers, on_delete = models.CASCADE)
    product = models.ForeignKey(Products, on_delete = models.CASCADE) 
    quantity = models.PositiveIntegerField(default = 1) 

    def clean(self):
        if self.quantity > self.product.product_quantity: 
            raise ValidationError("Quantity exceeds availvable stock.!!") 
        
    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)