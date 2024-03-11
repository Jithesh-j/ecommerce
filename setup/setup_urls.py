from django.urls import path
from django.contrib import admin
from . import views

admin.site.site_header = "Admin"
admin.site.site_title = "Admin Site" 
admin.site.index_title = "Welcome"
urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.user_login, name ='login'),
    path("logout/", views.user_logut, name= "logout"),
    path("register/",views.register_user, name = 'register'),
    # create a url for the product
    # if product is a 8 integer with primary key (pk) 8
    path("product/<int:pk>", views.product, name ='product'),
    path("category/<str:pc>", views.category, name ='category'),
    path("update_user/", views.update_user, name='update_user'),
    path("update_password/", views.update_password, name ='update_password'),
    path("update_profile_info/", views.update_profile_info, name ='update_profile_info'),
    path("search/", views.search, name ='search-1'),

]