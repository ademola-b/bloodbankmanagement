from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=[('admin', 'Admin'),('donor', 'Donor'), ('patient','Patient'), ], default="patient")
