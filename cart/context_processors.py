from .cart import Cart

#Create context processor on all pages
def cart(request):
    return {'cart': Cart(request)}
