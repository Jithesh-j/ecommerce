import json
from setup.forms import UpdateProfileInfo
from setup.models import Customer_Profile, Product


class Cart():  
    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.cart_key = 'cart'

        if self.cart_key not in request.session:
            request.session[self.cart_key] = {}
            
        self.cart = request.session[self.cart_key]
        self.load_user_cart()

    def load_user_cart(self):
        if self.request.user.is_authenticated:
            current_user = Customer_Profile.objects.filter(user__id=self.request.user.id).first()
            if current_user and current_user.cart_details:
                user_cart = json.loads(current_user.cart_details)
                self.cart.update(user_cart)
                self.session.modified = True

    def _save_cart_to_user_profile(self):
        if self.request.user.is_authenticated:
            current_user = Customer_Profile.objects.filter(user__id=self.request.user.id).first()
            if current_user:
                current_user.cart_details = json.dumps(self.cart)
                current_user.save()

    def product_exist(self, product):
        return str(product.id) in self.cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            self.cart[product_id] += int(product_qty)
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        self._save_cart_to_user_profile()

    def __len__(self):
        
        return len(self.cart)

    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_qty(self):
        return self.cart
    
    def empty(self):
        # Remove all items from the cart
        self.cart = {}
        self.cart.clear()
        self._save_cart_to_user_profile()
        self.session.modified = True

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        self.cart[product_id] = product_qty
        self.session.modified = True
        self._save_cart_to_user_profile()

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        self._save_cart_to_user_profile()

    def total_cart_cost(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value
        return total
    
