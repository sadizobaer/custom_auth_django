import json
import base64
import hashlib
import hmac
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"  # Replace with a strong, unique secret key


def generate_signature(encoded_header, encoded_payload):
    key = SECRET_KEY.encode()
    message = (encoded_header + "." + encoded_payload).encode()
    signature = base64.urlsafe_b64encode(hmac.new(key, message, hashlib.sha256).digest()).decode().rstrip("=")
    return signature


def verify_signature(encoded_header, encoded_payload, signature):
    expected_signature = generate_signature(encoded_header, encoded_payload)
    return hmac.compare_digest(expected_signature, signature)


def encode_jwt(payload):
    # Convert datetime to string representation
    payload["exp"] = (datetime.utcnow() + timedelta(days=1)).isoformat()

    header = {"alg": "HS256", "typ": "JWT"}
    encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")

    signature = generate_signature(encoded_header, encoded_payload)
    jwt_token = f"{encoded_header}.{encoded_payload}.{signature}"
    return jwt_token


def decode_jwt(jwt_token):
    encoded_header, encoded_payload, signature = jwt_token.split(".")
    header = json.loads(base64.urlsafe_b64decode(encoded_header + "==").decode())
    payload = json.loads(base64.urlsafe_b64decode(encoded_payload + "==").decode())

    if verify_signature(encoded_header, encoded_payload, signature):
        # Convert the expiration string back to datetime
        payload["exp"] = datetime.fromisoformat(payload["exp"])
        return payload
    else:
        raise ValueError("Invalid signature")


# Rest of your code...
