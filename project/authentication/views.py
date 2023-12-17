from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import (
    CustomUserSerializer,
    ObtainTokenPairSerializer,
    RefreshTokenSerializer,
)
from .jwt_util import generate_jwt_token, verify_jwt_token


class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)


class ObtainTokenPairView(generics.CreateAPIView):
    serializer_class = ObtainTokenPairSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user:
            token = generate_jwt_token(user)  # Your custom JWT creation logic
            return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class RefreshTokenView(generics.CreateAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]

        try:
            user_id = verify_jwt_token(
                refresh_token
            )  # Your custom JWT verification logic
            # Additional logic if needed with the user_id
        except Exception as e:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Your custom logic for token refreshing

        return Response({"success": "Token refreshed"}, status=status.HTTP_200_OK)
