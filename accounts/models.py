from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True)
    contact = models.CharField(max_length=100, blank=True)  # phone / LINE / WhatsApp, shown via "Contact Reporter"

    def __str__(self):
        return self.username