# models.py

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError


class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    idname = models.CharField(max_length=50, unique=True)
    phonenumber = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)  # Store the hashed passwords

    def create_user(email, idname, password):
        user = CustomUser(email=email, idname=idname, password=password)
        if not user.email or not user.idname:
            raise ValidationError("Email and idname are required fields.")
        user.save()

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.idname
