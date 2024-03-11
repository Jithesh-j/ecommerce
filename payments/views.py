from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
import stripe
from cart.cart import Cart


stripe.api_key = "sk_test_51OnuXdBQ3eXPnL9FSImr0dKfrqEtbBgEgNOpNvG309PrTZSl7WRNdbJZlocZVDYVqnUTPEh5wH9OmM36qPiUA42X00kBcDeG9C"

def create_payment_intent(request):
    amount = Cart.total_cart_cost()
    if request.method == 'POST':
        token = request.POST['stripeToken']
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                source=token,
            )
        except stripe.error.CardError as e:
            pass
    return JsonResponse({'client_secret': intent.client_secret})

def paymentsuccess(request):
    print("Payment Success View Reached")
    if request.method == 'POST':
        print("POST Request Received")
        print("Session Key:", request.session.session_key)
        print("Cart Data:", request.session.get('cart', {}))
        cart = Cart(request)
        cart.empty()
        print("Cart Cleared")
        return render(request, "paymentsuccess.html", {})

    


# class PaymentPage(TemplateView):
#     template_name = "payments.html"
