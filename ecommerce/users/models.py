from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse

class CustomUser(AbstractUser):

    def __str__(self):
        return f"{self.first_name} ({self.last_name})"
    
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    address_line_1 = models.CharField("Address line 1", max_length=128)
    address_line_2 = models.CharField("Address line 2", max_length=128, blank=True, null=True)
    city = models.CharField("City", max_length=100)
    state = models.CharField("State / Province", max_length=100)
    postal_code = models.CharField("Postal Code", max_length=20)
    country = models.CharField("Country", max_length=100, default='Colombia')
    is_default = models.BooleanField("Default Address", default=False)

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.state} {self.postal_code}"
    
    def get_absolute_url(self):
        return reverse('user_addresses')
    
    class Meta:
        # Enforce that an address must be unique for a user.
        # An address is considered unique if the combination of all its fields 
        # (from address_line_1 to country) is unique for a given user.
        unique_together = ('user', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country') 
        verbose_name_plural = 'Addresses'