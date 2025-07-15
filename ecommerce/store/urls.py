from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # create all categories urls
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)