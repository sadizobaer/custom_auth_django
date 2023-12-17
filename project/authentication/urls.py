# urls.py

from django.urls import path
from .views import RegisterUserView, ObtainTokenPairView, RefreshTokenView

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("token/", ObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
]
