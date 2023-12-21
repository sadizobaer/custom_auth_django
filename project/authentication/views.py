from django.contrib.auth.hashers import check_password
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer
from .myjwt import generate_jwt_token, verify_jwt_token


class RegisterUserView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "user_id": user.id,
                    "email": user.email,
                    "message": "User registered successfully!",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "error": "Invalid credentials",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginUserView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data["email"]
        password = request.data["password"]
        user = CustomUser.objects.get(email=email)
        if check_password(password, user.password):
            access_token = generate_jwt_token(user, token_type="access")
            refresh_token = generate_jwt_token(user, token_type="refresh")
            return Response(
                {
                    "message": "User logged in successfully!",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "error": "Invalid credentials",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )


class RefreshTokenView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {
                    "error": "Refresh token not provided.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_id = verify_jwt_token(refresh_token)
            user = CustomUser.objects.get(id=user_id)
            new_access_token = generate_jwt_token(user, token_type="access")
            new_refresh_token = generate_jwt_token(user, token_type="refresh")
            return Response(
                {
                    "message": "Token refreshed successfully!",
                    "access_token": new_access_token,
                    "refresh_token": new_refresh_token,
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {
                    "message": str(e),
                    "access_token": "",
                    "refresh_token": "",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
