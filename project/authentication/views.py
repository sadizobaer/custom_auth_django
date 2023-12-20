from django.contrib.auth.hashers import check_password
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer
from .myjwt import generate_jwt_token


class RegisterUserView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully!", "user_id": user.id},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginUserView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data["email"]
        password = request.data["password"]
        user = CustomUser.objects.get(email=email)
        if check_password(password, user.password):
            token = generate_jwt_token(user)
            return Response(
                {"message": "User logged in successfully!", "token": token},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
