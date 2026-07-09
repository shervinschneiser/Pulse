import hashlib
import hmac


def generate_signature(
    payload: bytes,
    secret: str,
) -> str:
    return hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()


def verify_signature(
    payload: bytes,
    secret: str,
    signature: str,
) -> bool:
    expected = generate_signature(payload, secret)

    return hmac.compare_digest(expected, signature)
