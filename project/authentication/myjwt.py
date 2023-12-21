import json
import base64
import hmac
import hashlib
from datetime import datetime, timedelta
from django.conf import settings


def generate_jwt_token(user, token_type="access"):
    issued_at = datetime.utcnow()
    expiration_time = issued_at + timedelta(days=1)  # Adjust the timedelta as needed
    expiration_timestamp = int(expiration_time.timestamp())

    header = {
        "alg": "HS256",
        "typ": "JWT",
    }
    payload = {
        "user_id": user.id,
        "id_name": user.id_name,
        "email": user.email,
        "phonenumber": user.phonenumber,
        "iat": int(issued_at.timestamp()),
        "exp": expiration_timestamp,
        "token_type": token_type,
    }

    header_b64 = base64url_encode(json.dumps(header).encode("utf-8"))
    payload_b64 = base64url_encode(json.dumps(payload).encode("utf-8"))

    # Create the signature
    signature_base = f"{header_b64}.{payload_b64}".encode("utf-8")
    secret = settings.SECRET_KEY.encode("utf-8")
    hash = hmac.new(secret, signature_base, hashlib.sha256)
    signature = base64url_encode(hash.digest())

    return f"{header_b64}.{payload_b64}.{signature}"


def base64url_encode(data):
    encoded = base64.urlsafe_b64encode(data).rstrip(b"=")
    return encoded.decode("utf-8")


def base64url_decode(data):
    padding = b"=" * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data.encode("utf-8") + padding)


def verify_jwt_token(token):
    header_b64, payload_b64, signature = token.split(".")
    header = json.loads(base64url_decode(header_b64).decode("utf-8"))
    payload = json.loads(base64url_decode(payload_b64).decode("utf-8"))
    message = f"{header_b64}.{payload_b64}".encode("utf-8")
    secret = settings.SECRET_KEY.encode("utf-8")
    hash = hmac.new(secret, message, hashlib.sha256)
    expected_signature = base64url_encode(hash.digest())

    if signature != expected_signature:
        raise ValueError("Invalid token")

    expiration_time = datetime.utcfromtimestamp(payload["exp"])
    if datetime.utcnow() > expiration_time:
        raise ValueError("Token has expired")

    if "token_type" in payload and payload["token_type"] != "refresh":
        raise ValueError("Access tokens are not allowed for this operation")

    return payload["user_id"]
