from django.db import models
import datetime

from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

# Customer Profile
class Customer_Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now = True)
    phone = models.CharField(max_length =20, blank =False)
    address = models.CharField(max_length =200, blank = False)
    city = models.CharField(max_length = 200, blank = False)
    state = models.CharField(max_length =20, blank =False)
    zipcode = models.CharField(max_length =20, blank =False)
    country = models.CharField(max_length =20, blank =False)
    cart_details = models.CharField(max_length =20, blank =True, null= True)
    
    def __str__(self) -> str:
        return self.user.username
    class Meta:
        verbose_name_plural = 'Customer Profiles'
    
# Creating profile when signup
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Customer_Profile(user = instance)  
        user_profile.save()
post_save.connect(create_profile, sender=User)


# Product Categories
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categroies'

# Customers
class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

# Products
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=300, default="", blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    # sale 
    is_sale = models.BooleanField(default = False)
    sale_price = models.DecimalField(default =0, decimal_places =2, max_digits =6 )

    def __str__(self):
        return self.name


# # Customer Orders
# class Order(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  
#     quantity = models.IntegerField(default=1)
#     address = models.CharField(max_length=100, default="", blank=True)
#     phone = models.CharField(max_length=20, default="", blank=True)
#     date = models.DateField(default=datetime.datetime.today)
#     status = models.BooleanField(default=False)

#     def __str__(self):
#         return str(self.product)  
