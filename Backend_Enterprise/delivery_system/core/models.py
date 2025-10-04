from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES=[
        ('customer','Customer'),
        ('vendor','Vendor'),
        ('driver','Driver'),
        ('admin','Admin'),
    ]

    role= models.CharField(max_length=20, choices=ROLE_CHOICES,default='customer')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # phone= models.CharField(max_length=15, blank=True, null=True)
    # address= models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} {self.role}"
    
# class Vendor(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='vendor_profile')
#     Restarent_name= models.CharField(max_length=255)
#     Location=models.CharField(max_length=255)
#     Contact_number= models.CharField(max_length=255)
# connectingh the user table to vendor above
# related_name is a Python/Django shortcut to access the linked object from the other model; it does not rename the database table.