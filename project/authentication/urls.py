from django.urls import path
from .views import LoginView, RegistrationView, RefreshTokenView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("refresh-token/", RefreshTokenView.as_view(), name="refresh_token"),
    # Add other URL patterns as needed
]
