from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.timezone import now

def default_expires_at():
    return now().replace(hour=23, minute=59, second=59)

class Business(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    password = models.CharField(max_length=15)


    def __str__(self):
        return self.name
    

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('inventory_manager', 'Inventory Manager'),
        ('cashier', 'Cashier'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier')
    business = models.ForeignKey('Business', on_delete=models.CASCADE, null=True, blank=True)  
    

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

class CashierLoginID(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expires_at)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return now() > self.expires_at
