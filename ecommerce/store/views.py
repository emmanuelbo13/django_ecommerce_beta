from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from .models import Product, Category

# Create your views here.
class IndexView(TemplateView):
    template_name = 'store/index.html'
    model = Product
    category = Category
    context_object_name = 'products'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category_slug = self.kwargs.get('slug')
        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            
            def get_all_descendants(cat):
                descendants = list(cat.children.all())
                for child in cat.children.all():
                    descendants.extend(get_all_descendants(child))
                return descendants

            all_child_categories = get_all_descendants(category)
            categories_to_filter = [category] + all_child_categories
            context['products'] = Product.objects.filter(category__in=categories_to_filter).distinct()
            context['current_category'] = category
        else:
            context['products'] = Product.objects.all()
        
        context['parent_categories'] = Category.objects.filter(parent=None)
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'store/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # This gets the category object the view is displaying
        category = self.get_object()

        # Helper function to recursively get all child categories
        def get_all_descendants(cat):
            descendants = list(cat.children.all())
            for child in cat.children.all():
                descendants.extend(get_all_descendants(child))
            return descendants

        # Get the list of all categories to filter by
        all_child_categories = get_all_descendants(category)
        categories_to_filter = [category] + all_child_categories
        
        # Filter products belonging to the main category or any of its descendants
        context['products'] = Product.objects.filter(category__in=categories_to_filter).distinct()
        
        return context