from django.contrib import admin
from .models import Category, Product

class TopLevelCategoryListFilter(admin.SimpleListFilter):
    title = 'Top-level category'
    parameter_name = 'top_level'

    def lookups(self, request, model_admin):
        # Only show top-level categories (parent=None)
        top_levels = Category.objects.filter(parent=None)
        return [(cat.id, cat.name) for cat in top_levels]

    def queryset(self, request, queryset):
        if self.value():
            # Get all descendants for the selected top-level category
            top_cat = Category.objects.get(id=self.value())
            def get_all_descendants(cat):
                descendants = list(cat.children.all())
                for child in cat.children.all():
                    descendants.extend(get_all_descendants(child))
                return descendants
            all_cats = [top_cat] + get_all_descendants(top_cat)
            return queryset.filter(id__in=[cat.id for cat in all_cats])
        return queryset

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')  # Added 'slug' to the list display
    list_filter = (TopLevelCategoryListFilter,)

admin.site.register(Category, CategoryAdmin)

class ProductSlugFirstCharFilter(admin.SimpleListFilter):
    title = 'Slug first character'
    parameter_name = 'slug_first_char'

    def lookups(self, request, model_admin):
        # Get all unique first characters from product slugs
        chars = set(Product.objects.exclude(slug__isnull=True).exclude(slug__exact='').values_list('slug', flat=True))
        first_chars = sorted(set(slug[0].lower() for slug in chars if slug))
        return [(char, char.upper()) for char in first_chars]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(slug__istartswith=self.value())
        return queryset

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price')
    list_filter = (ProductSlugFirstCharFilter,)

admin.site.register(Product, ProductAdmin)

#