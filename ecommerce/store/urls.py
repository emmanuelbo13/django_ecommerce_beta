from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # create all categories urls
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    # products
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    # cart
    path('cart/', views.CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('checkout/shipping', views.CheckoutView.as_view(), name='checkout_shipping'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)