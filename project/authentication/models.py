# models.py

from django.db import models


class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    id_name = models.CharField(max_length=50, unique=True)
    phonenumber = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)  # Store the hashed passwords

    def __str__(self):
        return self.email
