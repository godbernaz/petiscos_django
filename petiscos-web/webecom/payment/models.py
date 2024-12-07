from django.db import models
from django.contrib.auth.models import User
from mystore.models import Products
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.pt.forms import PTZipCodeField
from localflavor.pt.pt_regions import REGION_CHOICES

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_phone = PhoneNumberField(blank=True, null=True) 
    shipping_email = models.EmailField(max_length=255)  
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=200, blank=True, choices=REGION_CHOICES)
    shipping_zipcode = models.CharField(max_length=8, validators=[PTZipCodeField().validators[0]], blank=False)
    shipping_country = models.CharField(max_length=255, default="Portugal")

    class Meta:
        verbose_name_plural = "Shipping Address"
        
    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
def create_shipping(sender, instance, created, **kwargs):
    if created: 
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()
        
post_save.connect(create_shipping, sender=User)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = PhoneNumberField(null=True, blank=True)
    address = models.CharField(max_length=100, default='', blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f'Order - {str(self.id)}'
    
# Creating a Shipping Date automatically
@receiver(pre_save, sender=Order)
def set_shipped_date(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()   
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'Order Items - {str(self.id)}'
    