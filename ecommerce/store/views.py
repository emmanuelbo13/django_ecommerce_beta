from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from .models import Product, Category

# Create your views here.

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

        # category_slug = self.kwargs.get('slug')

        # If a category slug is provided in the URL, filter products by that category and its children.
        # this is useful to allow inclusion of other paths like 'women/sport-fits' 
        # if category_slug:
        #     # Get the category object based on the slug provided in the URL.
        #     # If the category does not exist, a 404 error will be raised.
        #     # This ensures that the view only processes valid categories.
        #     category = get_object_or_404(Category, slug=category_slug)
        #     # Recursive function to get all child categories 
        #     def get_all_descendants(cat):
        #         # Get all direct children of the current category and then recursively get their children.
        #         # This builds a flat list of all descendant categories.
        #         descendants = list(cat.children.all())
        #         for child in cat.children.all():
        #             # Extend the list with descendants of each child category.
        #             descendants.extend(get_all_descendants(child))
        #         return descendants
            
        #     # Get all descendants of the selected category.
        #     all_child_categories = get_all_descendants(category)
        #     # Create a list of categories to filter products by, including the selected category and all its children.
        #     categories_to_filter = [category] + all_child_categories
        #     # Filter products to find all that belong to the selected category or its children.
        #     context['products'] = Product.objects.filter(category__in=categories_to_filter).distinct()
        # else:
        #     # If no category slug is provided, show all products.
        #     context['products'] = Product.objects.all().distinct()
        
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