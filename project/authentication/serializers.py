# serializers.py

from rest_framework import serializers
from .models import CustomUser
from .jwt_util import generate_jwt_token, verify_jwt_token, custom_authenticate


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "idname", "phonenumber", "profilepic", "password")
        extra_kwargs = {"password": {"write_only": True}}


class ObtainTokenPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    token = (
        serializers.SerializerMethodField()
    )  # Rename 'tokens' to 'token' for consistency

    def get_token(self, user):  # Rename 'get_tokens' to 'get_token'
        return generate_jwt_token(user)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = custom_authenticate(email=email, password=password)

        if user and user.is_active:
            data["user"] = user
        else:
            raise serializers.ValidationError("Invalid credentials")

        return data


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh_token = data.get("refresh")

        try:
            user_id = verify_jwt_token(refresh_token)
            # Additional logic if needed with the user_id
        except Exception as e:
            raise serializers.ValidationError("Invalid refresh token")

        return data
