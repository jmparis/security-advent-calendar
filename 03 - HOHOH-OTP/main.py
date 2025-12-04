import argparse # To parse command-line arguments
from datetime import datetime, timezone
from src.generate_totp_tokens import generate_totp_tokens

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
            try:
                custom_datetime = datetime.strptime(args.time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                time_parts = datetime.strptime(args.time, "%H:%M:%S").time()
                today = datetime.now().date()
                custom_datetime = datetime.combine(today, time_parts)
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
