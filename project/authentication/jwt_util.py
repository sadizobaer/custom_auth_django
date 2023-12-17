# jwt_util.py
from .myjwt import generate_jwt_token, verify_jwt_token
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY


def generate_jwt_token(user):
    payload = {"user_id": user.id, "exp": datetime.utcnow() + timedelta(days=1)}
    return generate_jwt_token(payload, SECRET_KEY, algorithm="HS256").decode("utf-8")


def verify_jwt_token(token):
    try:
        payload = verify_jwt_token(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        return None


def custom_authenticate(email, password):
    user = authenticate(email=email, password=password)
    return None
