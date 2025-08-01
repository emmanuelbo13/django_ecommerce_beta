from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    # Add the logout URL.
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfile.as_view(), name='user_profile'),
    path('addresses/create/', views.CreateUserAddress.as_view(), name='create_address'),
    path('addresses/', views.UserAddressesList.as_view(), name='user_addresses'),
    path('addresses/<int:pk>/update', views.UpdateAddress.as_view(), name='update_address'),
    path('addresses/<int:pk>/delete', views.DeleteAddress.as_view(), name='delete_address')
]