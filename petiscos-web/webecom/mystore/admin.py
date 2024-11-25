from django.contrib import admin
from .models import Categories, Customers, Products, Orders, Profile
from django.contrib.auth.models import User

admin.site.register(Profile)
admin.site.register(Categories)
admin.site.register(Customers)
admin.site.register(Products)
admin.site.register(Orders)

# Mixing Profile + User Information
class ProfileInline(admin.StackedInline):
    model = Profile
    
# Extend User Model
class UserAdmin(admin.ModelAdmin): 
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]
    
admin.site.unregister(User)

admin.site.register(User, UserAdmin)