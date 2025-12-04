def truncate_dynamically(hash: bytes):
    """Truncates a generated HMAC hash and returns it as an integer"""
    offset = hash[-1] & 0x0F
    truncated = hash[offset:offset + 4]
    code_number = int.from_bytes(truncated, byteorder='big')
    return code_number & 0x7FFFFFFF

