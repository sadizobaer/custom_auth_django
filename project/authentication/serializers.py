# serializers.py
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "idname", "phonenumber", "password"]

    def create(self, validated_data):
        hashed_pwd = make_password(validated_data["password"])
        user = CustomUser.objects.create(
            email=validated_data["email"],
            password=hashed_pwd,
            idname=validated_data["idname"],
            phonenumber=validated_data["phonenumber"],
        )
        return user
