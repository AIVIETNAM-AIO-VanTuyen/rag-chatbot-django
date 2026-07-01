from django.db import models
from django.contrib.auth.models import User  

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='account')
    
    phone_number = models.CharField(max_length=10, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return f"Account of {self.user}"
