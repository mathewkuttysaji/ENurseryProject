from collections.abc import Iterable
from django.db import models
from django.core.validators import MinValueValidator
from PIL import Image

# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    product_quantity = models.PositiveIntegerField() 
    product_image = models.ImageField(upload_to='product_images/') 

    def __str__(self):
       return self.product_name  

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.product_image.path)
        new_size = (450, 450) 
        img.thumbnail(new_size)
        img.save(self.product_image.path)