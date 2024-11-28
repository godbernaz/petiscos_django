from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

# Register ShippingAddress model in Admin section.

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
