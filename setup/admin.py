from django.contrib import admin
from .models import Category, Customer,Product,Customer_Profile
from django.contrib.auth.models import User  
# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
# admin.site.register(Order)
admin.site.register(Customer_Profile)

class Profile_Details(admin.StackedInline):
    model = Customer_Profile
class UserAdmin(admin.ModelAdmin):
    model = User
    fields=["username","first_name","last_name","email"]
    inlines = [Profile_Details]

#unregister old way
admin.site.unregister(User)

#register new way
admin.site.register(User, UserAdmin)

