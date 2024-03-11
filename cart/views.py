from django.shortcuts import redirect, render, get_object_or_404

from setup.forms import UpdateProfileInfo
from .cart import Cart
from setup.models import Customer_Profile, Product
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.decorators import login_required

def cart_summary(request):
    try:
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_qty()
        total_cost = cart.total_cart_cost()
        return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": total_cost})
    except Exception as e:
        messages.error(request, f"Error retrieving cart summary: {e}")
        return redirect('home')


@login_required (login_url="login")  
def cart_checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_qty()
    total_cost = cart.total_cart_cost()
    return render(request, "checkout.html",{"cart_products": cart_products, "quantities": quantities, "totals": total_cost})

def payment(request):
    return render(request, "payments.html",{})

def cart_add(request):
    try:
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            product = get_object_or_404(Product, id=product_id)

            # Check if the product is already in the cart
            if cart.product_exist(product):
                messages.info(request, "Item is already in the cart.")
            else:
                cart.add(product=product, quantity=product_qty)
                card_quantity = cart.__len__()
                response = JsonResponse({'qty': card_quantity})
                messages.success(request, "Item Added to Cart Successfully.")
                return response
    except (ObjectDoesNotExist, ValueError, Exception) as e:
        messages.error(request, f"Error adding item to cart: {e}")

    return JsonResponse({'error': 'Failed to add item to cart'})

def cart_delete(request):
    try:
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            cart.delete(product=product_id)
            response = JsonResponse({'product': product_id})
            messages.success(request, "Your item has been deleted Successfully....!!")
            return response
    except (ObjectDoesNotExist, ValueError, Exception) as e:
        messages.error(request, f"Error deleting item from cart: {e}")
        return JsonResponse({'error': str(e)})

def cart_update(request):
    try:
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            cart.update(product=product_id, quantity=product_qty)
            response = JsonResponse({'qty': product_qty})
            messages.success(request, "Cart Updated Successfully....!")
            return response
    except (ObjectDoesNotExist, ValueError, ValidationError, Exception) as e:
        messages.error(request, f"Error updating cart: {e}")
        return JsonResponse({'error': str(e)})
    
def orderhistory(request):
    return render(request, "orderhistory.html",{})