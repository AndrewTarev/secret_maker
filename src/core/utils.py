import hashlib
import hmac


def hmac_passphrase(passphrase: str, secret: str) -> str:
    """Hashing a passphrase using HMAC"""
    return hmac.new(secret.encode(), passphrase.encode(), hashlib.sha256).hexdigest()
