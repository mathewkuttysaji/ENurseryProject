from collections.abc import Iterable
from django.db import models, transaction
from django.core.validators import MinValueValidator
from PIL import Image 
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image 
import os 
from accounts.models import Customers 
from django.core.exceptions import ValidationError 

class Products(models.Model):
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    product_quantity = models.PositiveIntegerField() 
    product_image = models.ImageField(upload_to='product_images/') 

    def __str__(self):
        return self.product_name  

@receiver(post_save, sender=Products)
def resize_product_image(sender, instance, created, **kwargs):
    if created:
        img = Image.open(instance.product_image.path)
        new_size = (450, 450) 
        img.thumbnail(new_size) 

        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Save the image with a .jpg extension
        image_path, image_extension = os.path.splitext(instance.product_image.path)
        new_image_path = f"{image_path}.jpg"
        img.save(new_image_path)

        # Update the product_image field with the new file path
        instance.product_image.name = f"product_images/{instance.pk}.jpg"
        instance.save()
        img.save(instance.product_image.path)


class Purchase(models.Model):
    customer = models.ForeignKey(Customers, on_delete = models.CASCADE) 
    products = models.ManyToManyField(Products, through='PurchaseItem') 
    total_amount = models.DecimalField(max_digits = 12, decimal_places = 3, validators = [MinValueValidator(0)]) 
    purchase_date = models.DateTimeField(auto_now_add = True) 
    address = models.TextField(blank=True) 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE) 
    product = models.ForeignKey(Products, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField() 
    unit_price = models.DecimalField(max_digits= 10, decimal_places=2, validators=[MinValueValidator(0)]) 

    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs) 


@receiver(post_save, sender=PurchaseItem)
def update_quantity(sender, instance, created, **kwargs): 
    if created:
        product = instance.product 
        product.product_quantity -= instance.quantity 
        product.save()