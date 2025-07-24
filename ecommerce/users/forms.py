from django import forms
from .models import CustomUser, Address

# Using forms.ModelForm provides more flexibility than UserCreationForm.
class CustomUserCreationForm(forms.ModelForm):
    # Explicitly define the password field with a PasswordInput widget 
    # to ensure the input is masked.
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        # Associate the form with the CustomUser model.
        model = CustomUser
        # Define the fields to be displayed in the form.
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def save(self, commit=True):
        # Override the save method to handle password hashing.
        user = super().save(commit=False)
        # Use set_password() to securely hash the password 
        # before saving it to the database.
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
        
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country', 'is_default']
        widgets = {
            'address_line_1': forms.TextInput(attrs={'placeholder': 'Address Line 1'}),
            'address_line_2': forms.TextInput(attrs={'placeholder': 'Address Line 2'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
        }

    def save(self, commit=True):
        # Override the save method to set the user field.
        address = super().save(commit=False)
        # Set the user to the currently logged-in user
        if address.is_default:
            # Ensure only one address can be default for the user
            # If the address is marked as default, unset the previous default address.
            # This ensures that the user can only have one default address.
            Address.objects.filter(user=address.user).update(is_default=False)

        if commit:
            address.save()
        return address