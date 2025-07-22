from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'first_name', 'last_name', 'email', 'phone_number',
            'address_line_1', 'address_line_2', 'city', 'state_province',
            'zip_postal_code', 'country', 'profile_picture'
        )