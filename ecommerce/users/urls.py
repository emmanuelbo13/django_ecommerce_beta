from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    # Add the logout URL.
    path('logout/', views.LogoutView.as_view(), name='logout'),
]