from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse
from decimal import Decimal

from .models import Product, Category, Order, OrderItem
from users.models import Address
from .cart import Cart
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from .mercadopago_service import MercadoPagoService
from .models import Order

# --- IndexView ---
# This view handles the main page of the store.
# It can display all products or filter them based on a selected category and its children.
class IndexView(TemplateView):
    # Specifies the template file to be rendered for this view.
    template_name = 'store/index.html'
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().distinct()  # All products by default
        context['categories'] = Category.objects.all()          # All categories

        parent_categories = Category.objects.filter(parent=None) # Top-level categories (e.g., Women, Men, Kids)

        # Recursive function to get all descendants of a category
        def get_all_descendants(cat):
            descendants = list(cat.children.all())
            for child in cat.children.all():
                descendants.extend(get_all_descendants(child))
            return descendants

        parent_products = {}  # Dictionary to hold products for each parent category (by slug)
        for parent in parent_categories:
            # Get all categories under this parent (including itself and all descendants)
            all_cats = [parent] + get_all_descendants(parent)
            print(f"Categories for {parent.name}: {all_cats}")
            # Query products in any of these categories
            parent_products[parent.slug] = Product.objects.filter(category__in=all_cats).distinct()
            print(f"parent_products dictionary after processing {parent.name}: {parent_products}")

        context['parent_categories'] = parent_categories      # Pass parent categories to template
        context['parent_products'] = parent_products          # Pass mapping of parent slug to products
        
        context['parent_categories'] = Category.objects.filter(parent=None)

        return context

# --- CategoryDetailView ---
# This view displays the products for a single category.
class CategoryDetailView(DetailView):
    # The model this view is based on. Django's DetailView handles fetching the object.
    model = Category
    # The template to render.
    template_name = 'store/category_detail.html'
    # The name of the variable in the template for the category object itself.
    context_object_name = 'category'

    # Add extra context to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the category object that this view is currently displaying.
        category = self.get_object()

        # --- Recursive helper function to get all child categories ---
        # This is the same logic as in IndexView to ensure consistent product filtering.
        def get_all_descendants(cat):
            descendants = list(cat.children.all())
            for child in cat.children.all():
                descendants.extend(get_all_descendants(child))
            return descendants

        # Get all descendants for the current category.
        all_child_categories = get_all_descendants(category)
        # Create the full list of categories to filter by.
        categories_to_filter = [category] + all_child_categories
        
        # Filter products to find all that belong to this category or its children.
        context['products'] = Product.objects.filter(category__in=categories_to_filter).distinct()
        
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the product object that this view is currently displaying.
        product = self.get_object()
        # Add the product to the context.
        context['product'] = product
        return context

class CartDetailView(View):
    # Display the cart contents.
    template_name = 'store/cart_detail.html'
    def get(self, request, *args, **kwargs):
        # Initialize the cart using the Cart class.
        cart = Cart(request)
        return render(request, self.template_name, {'cart':cart}) 

class AddToCartView(View):
    # add a product to the cart
    def post(self, request, product_id, *args, **kwargs):
        # Get the product ID from the POST data.
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        # Get the quantity from the POST data, defaulting to 1 if not provided.
        quantity = int(request.POST.get('quantity', 1))
        # Add the product to the cart.
        # Check if the quantity should be overridden. The value from the form is a string.
        override = request.POST.get('override_quantity', 'False').lower() in ('true', '1', 't')
        cart.add(product=product, quantity=quantity, override_quantity=override)
        # Redirect to the cart detail view.
        return redirect('store:cart_detail')
    
class RemoveFromCartView(View):
    # remove a product from the cart
    def post(self, request, product_id, *args, **kwargs):
        # Get the product ID from the POST data.
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        # Remove the product from the cart.
        cart.remove(product=product)
        # Redirect to the cart detail view.
        return redirect('store:cart_detail')

class CheckoutView(LoginRequiredMixin, View):
    """
    Handles the multi-step checkout process.
    Step 1: Shipping address selection.
    """
    template_name = 'store/checkout.html'
    login_url = '/users/login/' # Redirect here if user is not logged in

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for the shipping address selection page.
        """
        cart = Cart(request)
        if not cart:
            # If the cart is empty, there's nothing to check out.
            # Redirect to the main store page.
            return redirect('store:index')

        # Get all addresses associated with the currently logged-in user.
        addresses = Address.objects.filter(user=request.user)

        context = {
            'cart': cart,
            'addresses': addresses
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests when the user selects a shipping address.
        """
        cart = Cart(request)
        if not cart:
            return redirect('store:index')

        # Get the ID of the selected address from the form submission.
        selected_address_id = request.POST.get('shipping_address')

        if not selected_address_id:
            # If no address was selected, re-render the page with an error.
            # (This is a basic way to handle it; you could add a Django message.)
            addresses = Address.objects.filter(user=request.user)
            context = {
                'cart': cart,
                'addresses': addresses,
                'error': 'Please select a shipping address.'
            }
            return render(request, self.template_name, context)

        # Store the selected address ID in the user's session.
        # This allows the next step (payment) to know which address was chosen.
        request.session['shipping_address_id'] = int(selected_address_id)
        
        # Redirect to the payment page
        return redirect('store:checkout_payment')

class PaymentView(LoginRequiredMixin, View):
    template_name = 'store/payment.html'
    login_url = '/users/login/'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        if not cart:
            return redirect('store:index')

        shipping_address_id = request.session.get('shipping_address_id')
        if not shipping_address_id:
            return redirect('store:checkout_shipping')

        shipping_address = get_object_or_404(Address, id=shipping_address_id)

        context = {
            'cart': cart,
            'shipping_address': shipping_address,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if not cart:
            return redirect('store:index')

        shipping_address_id = request.session.get('shipping_address_id')
        if not shipping_address_id:
            return redirect('store:checkout_shipping')

        shipping_address = get_object_or_404(Address, id=shipping_address_id)

        # Create Order
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            total_price=cart.get_total_price(),
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['product'].price,
                quantity=item['quantity'],
            )

        mp_service = MercadoPagoService()
        preference_response = mp_service.create_preference(cart, shipping_address)

        if preference_response['status'] == 201:
            preference_data = preference_response['response']
            order.payment_id = preference_data['id']
            order.save()
            return redirect(preference_data['init_point'])
        else:
            # Handle error, e.g., log the error and redirect to a failure page
            print(f"Mercado Pago preference creation failed: {preference_response}")
            return redirect('store:payment_failure')

class PaymentSuccessView(TemplateView):
    template_name = 'store/payment_success.html'

class PaymentFailureView(TemplateView):
    template_name = 'store/payment_failure.html'

class PaymentPendingView(TemplateView):
    template_name = 'store/payment_pending.html'

@csrf_exempt
def mercadopago_webhook(request):
    if request.method == 'POST':
        data = request.json
        if data.get('type') == 'payment':
            payment_id = data['data']['id']
            mp_service = MercadoPagoService()
            payment_status = mp_service.get_payment_status(payment_id)

            try:
                order = Order.objects.get(payment_id=payment_id)
                order.status = payment_status
                order.save()
            except Order.DoesNotExist:
                pass

        return JsonResponse({'status': 'ok'})
    return HttpResponseBadRequest()
