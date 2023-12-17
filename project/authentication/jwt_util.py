# jwt_util.py
from .myjwt import encode_jwt, decode_jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"


def create_jwt_token(user):
    payload = {"user_id": user.id, "exp": datetime.utcnow() + timedelta(days=1)}
    return encode_jwt(payload, SECRET_KEY, algorithm="HS256").decode("utf-8")


def decode_jwt_token(token):
    try:
        payload = decode_jwt(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        return None
