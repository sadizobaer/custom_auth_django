# utils.py

import json
import base64
from datetime import datetime, timedelta
from django.conf import settings
from .models import CustomUser

SECRET_KEY = settings.SECRET_KEY


def base64url_encode(data):
    encoded = base64.urlsafe_b64encode(data).rstrip(b"=")
    return encoded.decode("utf-8")


def base64url_decode(data):
    padding = b"=" * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)


def generate_jwt_token(user):
    issued_at = datetime.utcnow()
    expiration_time = issued_at + timedelta(days=1)

    header = {
        "alg": "HS256",
        "typ": "JWT",
    }

    payload = {
        "user_id": user.id,
        "iat": issued_at,
        "exp": expiration_time,
    }

    header_b64 = base64url_encode(json.dumps(header).encode("utf-8"))
    payload_b64 = base64url_encode(json.dumps(payload).encode("utf-8"))

    signature = base64url_encode(
        settings.SECRET_KEY.encode("utf-8")
        + ".".encode("utf-8")
        + header_b64.encode("utf-8")
        + ".".encode("utf-8")
        + payload_b64.encode("utf-8")
    )

    return f"{header_b64}.{payload_b64}.{signature}"


def verify_jwt_token(token):
    try:
        header_b64, payload_b64, signature = token.split(".")
        header = json.loads(base64url_decode(header_b64).decode("utf-8"))
        payload = json.loads(base64url_decode(payload_b64).decode("utf-8"))

        # Validate the signature (optional but recommended)
        expected_signature = base64url_encode(
            settings.SECRET_KEY.encode("utf-8")
            + ".".encode("utf-8")
            + header_b64.encode("utf-8")
            + ".".encode("utf-8")
            + payload_b64.encode("utf-8")
        )

        if signature != expected_signature:
            raise ValueError("Invalid signature")

        # Validate expiration time (optional but recommended)
        expiration_time = datetime.utcfromtimestamp(payload["exp"])
        if datetime.utcnow() > expiration_time:
            raise ValueError("Token has expired")

        return payload["user_id"]

    except Exception as e:
        raise ValueError("Invalid token") from e
