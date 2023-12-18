from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class CustomerManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user
    
    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class Customers(AbstractUser):

    username = None
    last_name = None
    first_name = None

    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=10)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ ]