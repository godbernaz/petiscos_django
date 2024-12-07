from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_quill.fields import QuillField
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.pt.forms import PTZipCodeField
from localflavor.pt.pt_regions import REGION_CHOICES

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    phone = PhoneNumberField(blank=True) 
    address1 = models.CharField(max_length=25, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True, choices=REGION_CHOICES)
    zipcode = models.CharField(max_length=8, blank=True, validators=[PTZipCodeField().validators[0]])
    country = models.CharField(max_length=255, default="Portugal")
    old_cart = models.CharField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

# Signal to automatically create the profile when creating a user
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)
    
# Categories of products
class Categories(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

# Customer details
class Customers(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(max_length=15)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)  

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name_plural = "Customers"
    
# List of products.
class Products(models.Model):
    name = models.CharField(max_length=100)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='EUR')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)
    description = QuillField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Products" 
    
# Customer order details
class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product
    
    class Meta:
        verbose_name_plural = "Orders" 