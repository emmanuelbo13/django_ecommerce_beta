from django import forms
from .models import CustomUser

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
        