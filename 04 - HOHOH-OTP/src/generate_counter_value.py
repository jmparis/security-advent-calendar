from math import floor
import time

VALIDITY_DURATION = 30

def generate_counter_value(custom_timestamp: float = None):
    """Generates the counter-value for the TOTP algorithm's hash generator.
    If custom_timestamp is provided, it will be used instead of the current time."""
    if custom_timestamp is not None:
        timestamp = custom_timestamp
    else:
        timestamp = time.time()
    timestamp = floor(timestamp)
    counter_value = floor(timestamp / VALIDITY_DURATION)
    return counter_value
