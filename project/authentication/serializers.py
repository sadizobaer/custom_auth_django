# serializers.py
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser
import uuid


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "phonenumber", "password"]

    def create(self, validated_data):
        id_name_genarated = str(uuid.uuid4())
        hashed_pwd = make_password(validated_data["password"])
        user = CustomUser.objects.create(
            email=validated_data["email"],
            password=hashed_pwd,
            id_name=id_name_genarated,
            phonenumber=validated_data["phonenumber"],
        )
        return user
