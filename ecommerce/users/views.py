from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from .models import Address  # Assuming you have an Address model defined
from .forms import CustomUserCreationForm, AddressForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Import Django's built-in authentication form and login/logout functions
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login') # Redirect to login page on successful registration

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

# This class handles the login process.
class LoginView(View):
    template_name = 'users/login.html'
    # Redirect to the homepage on successful login.
    success_url = reverse_lazy('store:index')

    def get(self, request, *args, **kwargs):
        # When a user visits the login page, display the authentication form.
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # When the user submits the form, process the credentials.
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # If the form is valid, authenticate the user.
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # If authentication is successful, log the user in.
                login(request, user)
                return redirect(self.success_url)
        # If the form is invalid, re-render the page with the form and errors.
        return render(request, self.template_name, {'form': form})

# This class handles the logout process.
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        # When a user accesses this view, log them out.
        logout(request)
        # Redirect to the login page after logging out.
        return redirect(reverse_lazy('users:login'))

class UserProfile(View):
    template_name = 'users/user_profile.html'

    def get(self, request, *args, **kwargs):
        # Render the user's profile page.
        return render(request, self.template_name, {'user': request.user})

# USER ADDRESSES CRUD
class CreateUserAddress(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'users/create_address.html'
    success_url = reverse_lazy('users:user_addresses')
    success_message = "Address added successfully"
    login_url = reverse_lazy('login')  # Redirect to login if not authenticated

    def form_valid(self, form):
        # Set the user to the currently logged-in user
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, 'You have already saved this address.')
            return self.form_invalid(form)
    

class UserAddressesList(ListView):
    model = Address  
    template_name = 'users/addresses.html'
    context_object_name = 'addresses'
    login_url = reverse_lazy('users:login')  # Redirect to login if not authenticated

    def get_queryset(self):
        # Filter addresses by the logged-in user
        return Address.objects.filter(user=self.request.user)
    
class UpdateAddress(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'users/update_address.html'
    success_url = reverse_lazy('users:user_addresses')
    success_message = "Address was updated successfully"
    login_url = reverse_lazy('users:login')  # Redirect to login if not authenticated

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class DeleteAddress(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Address
    success_url = reverse_lazy('users:user_addresses')
    success_message = "Address was deleted successfully"
    login_url = reverse_lazy('users:login')  # Redirect to login if not authenticated

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
