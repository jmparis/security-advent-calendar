import time
from math import floor
import base64 # To convert the secret into the 20 random bytes
import hmac # Provides the HMAC algorithm
import hashlib # Provides the SHA1 algorithm
import argparse # To parse command-line arguments
from datetime import datetime, timezone

# By default, use a 30-seconds time window
VALIDITY_DURATION = 30

def generate_counter_value (custom_timestamp: float = None):
  """Generates the counter-value for the TOTP algorithm's hash generator.
  If custom_timestamp is provided, it will be used instead of the current time."""
  if custom_timestamp is not None:
    timestamp = custom_timestamp
  else:
    timestamp = time.time() # Gets current time as a float (= with microseconds)
  timestamp = floor(timestamp) # Turn it into an integer (= only seconds)
  # Doing the following ensures that the value increments by one every 30
  # seconds
  counter_value = floor(timestamp / VALIDITY_DURATION)
  return counter_value


def generate_hash (K: str, C: int):
  """Generates a TOTP compatible HMAC hash based on the shared secret (K) and
  the current time window/counter value C."""
  # Secrets are usually provided in base32 format, so we need to decode it
  # (cf. https://stackoverflow.com/a/57325779)
  key_bytes = base64.b32decode(K)
  # We have to specify how many bytes to use to represent the time. 8 means
  # 64 bit, which helps avoid the Y2k38 bug. Python will throw an error if the
  # number is too big to be represented.
  counter_bytes = C.to_bytes(8, byteorder = 'big')
  # Take the secret and the counter and generate a hash.
  hash = hmac.digest(key_bytes, counter_bytes, hashlib.sha1)
  # NOTE: The hash must be big endian. This code here assumes that
  # hmac.digest() always uses big endian.
  return hash


def truncate_dynamically (hash: bytes):
  """Truncates a generated HMAC hash and returns it as an integer"""
  # Extract the four least significant bits from the hash, which is by
  # definition between zero (0000) and 15 (1111)
  offset = hash[-1] & 0x0F
  # Extract four bytes, or 32 bits from the offset
  truncated = hash[offset:offset + 4]
  # Convert them into a number. The biggest number that can be represented in
  # 32 bit is 2,147,483,647.
  code_number = int.from_bytes(truncated, byteorder = 'big')
  # Return the least significant 31 bits. This here essentially removes bit 32
  # to avoid ambiguity with signed/unsigned integers, because the most
  # significant bit is usually 0 for a positive, and 1 for a negative number,
  # but there can be issues with that.
  return code_number & 0x7FFFFFFF


TOKEN_LENGTH = 6 # How many digits should each token have?

def truncated_hash_to_token (code: int, digits: int = TOKEN_LENGTH):
  """Takes a truncated HMAC code number and returns the modulo of that to
  return the requested number of digits"""
  code = code % 10 ** digits # This is basically a rounding up
  # NOTE: Sometimes the resulting code is less than the amount of digits. In
  # that case, we must left-pad with zeros.
  code = str(code)
  if len(code) < digits:
    code = code.rjust(digits, "0")
  return code


VALID_START = -2 # Allow 2 time steps in the past to be considered valid
VALID_END = 2 # Allow 2 time steps in the future to be considered valid

def generate_totp_tokens (
    key: str,
    timestep_start = VALID_START,
    timestep_end = VALID_END,
    custom_timestamp: float = None
):
  """Generates a list of valid tokens within the valid window provided."""
  tokens: list[str] = []
  counter_value = generate_counter_value(custom_timestamp)

  for timestep in range(timestep_start, timestep_end + 1):
    hm = generate_hash(key, counter_value + timestep)
    code = truncate_dynamically(hm)
    valid_token = truncated_hash_to_token(code)
    tokens.append(valid_token)

  return tokens


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="TOTP Token Generator/Validator")
  parser.add_argument(
    "--time", "-t",
    type=str,
    help="Date and time to use for TOTP calculation (format: YYYY-MM-DD HH:MM:SS or HH:MM:SS). Uses current time if not specified.",
    default=None
  )
  parser.add_argument(
    "--utc", "-u",
    action="store_true",
    help="Utiliser l'heure UTC pour le calcul du TOTP."
  )
  args = parser.parse_args()

  custom_timestamp = None
  if args.time:
    try:
      # Try to parse full date and time first
      try:
        custom_datetime = datetime.strptime(args.time, "%Y-%m-%d %H:%M:%S")
      except ValueError:
        # Fall back to time only, combined with today's date
        time_parts = datetime.strptime(args.time, "%H:%M:%S").time()
        today = datetime.now().date()
        custom_datetime = datetime.combine(today, time_parts)
      # Si l'option --utc est passée, forcer en UTC
      if args.utc:
        custom_datetime = custom_datetime.replace(tzinfo=timezone.utc)
      custom_timestamp = custom_datetime.timestamp()
      print(f"Using custom time: {custom_datetime} ({int(custom_timestamp)} seconds)")
    except ValueError:
      print("Invalid format. Please use YYYY-MM-DD HH:MM:SS or HH:MM:SS (e.g., 2025-12-04 14:30:00 or 14:30:00)")
      exit(1)
  else:
    if args.utc:
      current_time = datetime.now(timezone.utc)
    else:
      current_time = datetime.now()
    print(f"Using current time: {current_time} ({int(current_time.timestamp())} seconds)")

  secret = "F5TGYYLHNFZW433UNBSXEZJP"
  valid_tokens = generate_totp_tokens(secret, custom_timestamp=custom_timestamp)
  print(f"Valid tokens: {valid_tokens}")

  client_token = input("Enter TOTP code from device (Ctrl+C to abort): ")

  if client_token in valid_tokens:
    print("Token is valid!")
  else:
    print("Sorry, but the token is not valid.")
