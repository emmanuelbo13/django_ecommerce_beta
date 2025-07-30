# C:\Users\buste.LAPTOP-5ROA9SUG\OneDrive\Escritorio\CS1\django_ecommerce_beta\ecommerce\store\cart.py

from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart:
    """
    A class to manage the shopping cart in the session.
    The cart is stored in the session as a dictionary:
    {
        'product_id_1': {'quantity': X, 'price': 'Y.YY'},
        'product_id_2': {'quantity': A, 'price': 'B.BB'},
    }
    """
    def __init__(self, request):
        """
        Initialize the cart.
        """
        # Store the current session to make it accessible to other methods of the class.
        self.session = request.session
        # Try to get the cart from the current session.
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # If no cart is found in the session, create a new empty cart.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        # Convert the product ID to a string because Django uses JSON to serialize session data.
        product_id = str(product.id)

        # If the product is not in the cart, initialize it with the given quantity.
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        # If the user is updating the quantity from the cart page, override the existing quantity.
        elif override_quantity:
            self.cart[product_id]['quantity'] = quantity
        # Otherwise, add the new quantity to the existing one.
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()

    def save(self):
        """
        Mark the session as "modified" to make sure it gets saved.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Allow iterating over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        # Get the product objects and add them to the cart.
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        # get total order price
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total price of all items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove cart from session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()