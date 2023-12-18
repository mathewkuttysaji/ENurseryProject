from django.db import models

from accounts.models import Customers
# Create your models here.

class ContactUs(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE) 
    date = models.DateTimeField(auto_now_add=True) 
    message_text = models.TextField()
