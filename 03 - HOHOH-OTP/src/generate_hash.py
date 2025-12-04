import base64
import hmac
import hashlib

def generate_hash(K: str, C: int):
    """Generates a TOTP compatible HMAC hash based on the shared secret (K) and
    the current time window/counter value C."""
    key_bytes = base64.b32decode(K)
    counter_bytes = C.to_bytes(8, byteorder='big')
    hash = hmac.digest(key_bytes, counter_bytes, hashlib.sha1)
    return hash

