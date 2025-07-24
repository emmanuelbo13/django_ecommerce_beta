from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from users.models import CustomUser, Address

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'categories'
        unique_together = ('slug', 'parent',)    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name
        # k = self.parent
        # while k is not None:
        #     full_path.append(k.name)
        #     k = k.parent
        # return ' -> '.join(full_path[::-1])

    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # stock = models.PositiveIntegerField(default=0) Not sure if we need this field yet.

    class Meta:
        verbose_name_plural = 'Products' # define plural for admin site.
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
    
    def __str__(self):
        return self.name

    # def is_in_stock(self):
    #     return self.stock > 0

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('store:order_detail', args=[self.id])

    def __str__(self):
        return f"Order {self.id} - {self.status}"
    
    class Meta:
        verbose_name_plural = 'Orders'
        verbose_name = 'Order'
        ordering = ('-created_at',)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name if self.product else 'Deleted Product'}"
    
    def get_total_item_price(self):
        return self.price * self.quantity
    
    class Meta:
        verbose_name_plural = 'Order Items'
        verbose_name = 'Order Item'
        ordering = ('-order__created_at',)
