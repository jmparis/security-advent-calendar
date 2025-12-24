import base58
encoded = "KkYWdtT6Nh5epg9sS2w5JAu8pG"
try:
    decoded = base58.b58decode(encoded)
    print(f"Bytes: {decoded}")
    print(f"UTF-8: {decoded.decode('utf-8', errors='ignore')}")
    print(f"ASCII: {decoded.decode('ascii', errors='ignore')}")
except Exception as e:
    print(f"Erreur: {e}")

data = b'flag<\xe2w\xd8\xac\x1a<l\x19d\x8dq]O\x01'
hex_string = data.hex()
print(hex_string)
