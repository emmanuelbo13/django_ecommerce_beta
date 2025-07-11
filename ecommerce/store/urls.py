from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('women/', views.IndexView.as_view(), {'slug': 'women'}, name='women_products'),
    path('men/', views.IndexView.as_view(), {'slug': 'men'}, name='men_products'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
]