from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Product, Category

# Create your views here.
class IndexView(TemplateView):
    template_name = 'store/index.html'
    model = Product
    category = Category
    context_object_name = 'products'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['categories'] = Category.objects.all()
        return context


