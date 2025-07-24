from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):

    def __str__(self):
        return f"{self.first_name} ({self.last_name})"
    
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    address_line_1 = models.CharField("Address line 1", max_length=255)
    address_line_2 = models.CharField("Address line 2", max_length=255, blank=True, null=True)
    city = models.CharField("City", max_length=100)
    state = models.CharField("Postal Code", max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField("Country", max_length=100, default='Colombia')
    is_default = models.BooleanField("Default Address", default=False)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"
    
    class Meta:
        unique_together = ('user', 'address_line_1', 'city', 'postal_code') 
        verbose_name_plural = 'Addresses'