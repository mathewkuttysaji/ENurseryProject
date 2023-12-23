from collections.abc import Iterable
from django.db import models
from django.core.validators import MinValueValidator
from PIL import Image 
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

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
        img.save(instance.product_image.path)
