TOKEN_LENGTH = 6

def truncated_hash_to_token(code: int, digits: int = TOKEN_LENGTH):
    """Takes a truncated HMAC code number and returns the modulo of that to
    return the requested number of digits"""
    code = code % 10 ** digits
    code = str(code)
    if len(code) < digits:
        code = code.rjust(digits, "0")
    return code

