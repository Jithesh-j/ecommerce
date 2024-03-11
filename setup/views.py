from django.shortcuts import redirect, render
from .models import Product, Category, Customer_Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ChangePasswordForm, SignUpForm, UpdateProfileInfo, UpdateUserForm
from django.db.models import Q

# Create your views here.

def index(request):
    try:
        products = Product.objects.all()
        return render(request, "index.html", {'products': products})
    except Exception as e:
        messages.error(request, f"Error fetching products: {e}")
        return redirect('home')  # Redirect to home or another appropriate page

def about(request):
    return render(request, "about.html", {})

def product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        return render(request, 'product.html', {'product': product})
    except Product.DoesNotExist:
        messages.error(request, "Oops! Product not found.")
        return redirect('index')

def category(request, pc):
    try:
        pc = pc.replace('-', ' ')
        category = Category.objects.get(name=pc)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect('index')

def user_login(request):
    try:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in!")
                return redirect('index')
            else:
                messages.error(request, "Invalid credentials. Please try again.")
                return redirect('login')
        else:
            return render(request, "login.html", {})
    except Exception as e:
        messages.error(request, f"Error during login: {e}")
        return redirect('index')

def user_logut(request):
    try:
        logout(request)
        messages.success(request, "You have been Successfully logged out.")
        return redirect('index')
    except Exception as e:
        messages.error(request, f"Error during logout: {e}")
        return redirect('index')

def register_user(request):
    try:
        form = SignUpForm()
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, "You have successfully registered!")
                messages.success(request, "Please update your Address/Shipping details")
                return redirect('update_profile_info')
            else:
                messages.error(request, "Registration unsuccessful. Please try again.")
                return redirect('register')
        else:
            return render(request, "register.html", {'form': form})
    except Exception as e:
        messages.error(request, f"Error during registration: {e}")
        return redirect('index')

def update_user(request):
    try:
        if request.user.is_authenticated:
            current_user = User.objects.get(id=request.user.id)
            user_form = UpdateUserForm(request.POST or None, instance=current_user)
            if user_form.is_valid():
                user_form.save()
                login(request, current_user)
                messages.success(request, "Details have been updated...")
                return redirect('index')
            return render(request, "update_user.html", {'user_form': user_form})
        else:
            messages.success(request, "Please login to update details....!")
            return redirect('index')
    except Exception as e:
        messages.error(request, f"Error updating user details: {e}")
        return redirect('index')

def update_profile_info(request):
    try:
        if request.user.is_authenticated:
            current_user = Customer_Profile.objects.get(user=request.user.id)
            profile_form = UpdateProfileInfo(request.POST or None, instance=current_user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Details have been updated...")
                return redirect('index')
            return render(request, "update_profile_info.html", {'profile_form': profile_form})
        else:
            messages.success(request, "Please login to update details....!")
            return redirect('index')
    except Exception as e:
        messages.error(request, f"Error updating profile details: {e}")
        return redirect('index')

def update_password(request):
    try:
        if request.user.is_authenticated:
            current_user = request.user
            if request.method == 'POST':
                password_form = ChangePasswordForm(current_user, request.POST)
                if password_form.is_valid():
                    password_form.save()
                    messages.success(request, "Your Password has been Updated, Login Again....")
                    return redirect('login')
                else:
                    for error in list(password_form.errors.values()):
                        messages.error(request, error)
                    return redirect('update_password')
            else:
                password_form = ChangePasswordForm(current_user)
                return render(request, "update_password.html", {'password_form': password_form})
        else:
            messages.success(request, "Please login to update your password")
            return redirect('index')
    except Exception as e:
        messages.error(request, f"Error updating password: {e}")
        return redirect('index')

def search(request):
    try:
        if request.method == "POST":
            searched = request.POST['searched']
            
            # Search by product name or category name
            products_details = Product.objects.filter(
                Q(name__icontains=searched) | Q(category__name__icontains=searched) | Q(description__icontains = searched)
            ).distinct()
            
            return render(request, 'search.html', {'searched': searched, 'products_details': products_details})
        else:
            return render(request, 'search.html', {})
    except Exception as e:
        messages.error(request, f"Error during search: {e}")
        return redirect('index')

