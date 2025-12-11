from src.generate_counter_value import generate_counter_value
from src.generate_hash import generate_hash
from src.truncate_dynamically import truncate_dynamically
from src.truncated_hash_to_token import truncated_hash_to_token

VALID_START = -2
VALID_END = 2

def generate_totp_tokens(
    key: str,
    timestep_start=VALID_START,
    timestep_end=VALID_END,
    custom_timestamp: float = None
):
    """Generates a list of valid tokens within the valid window provided."""
    tokens = []
    counter_value = generate_counter_value(custom_timestamp)
    for timestep in range(timestep_start, timestep_end + 1):
        hm = generate_hash(key, counter_value + timestep)
        code = truncate_dynamically(hm)
        valid_token = truncated_hash_to_token(code)
        tokens.append(valid_token)
    return tokens

