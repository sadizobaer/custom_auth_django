# models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


# class CustomUser(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#     idName = models.AutoField(unique=True, primary_key=True)
#     phoneNumber = models.CharField(max_length=15, unique=True)
#     profilePicUrl = models.URLField()
#     # Add other custom fields as needed
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["phoneNumber", "profilePicUrl"]

#     def __str__(self):
#         return self.email


class CustomUser(AbstractBaseUser):
    # ... other fields ...
    idName = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=15, unique=True)
    profilePicUrl = models.URLField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phoneNumber", "profilePicUrl"]

    def __str__(self):
        return self.email
