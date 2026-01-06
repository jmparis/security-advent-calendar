def xor_decode_move(encrypted_move, key):
    """Déchiffre le coup avec XOR"""
    decoded = ""
    decoded_bytes = []
    for char in encrypted_move:
        decoded_char = chr(ord(char) ^ key)
        decoded += decoded_char
        decoded_bytes.append(ord(char) ^ key)
    return decoded, decoded_bytes


def decode_name_alternative(name_encrypted, mystery_number):
    """Essaie différentes méthodes de déchiffrement"""
    results = {}

    # Méthode 1: Shift original
    shift = mystery_number % 8
    name1 = ""
    for value in name_encrypted:
        if shift == 0:
            name1 += chr(value)
        else:
            name1 += chr(value >> shift)
    results["shift"] = name1

    # Méthode 2: XOR avec mystery_number
    name2 = ""
    key = mystery_number & 0xFF  # Prendre seulement les 8 bits de poids faible
    for value in name_encrypted:
        name2 += chr(value ^ key)
    results["xor_low"] = name2

    # Méthode 3: XOR avec différentes parties du mystery_number
    for i, byte_key in enumerate([(mystery_number >> (8 * j)) & 0xFF for j in range(4)]):
        name3 = ""
        for value in name_encrypted:
            char_val = value ^ byte_key
            if 32 <= char_val <= 126:  # Caractères imprimables
                name3 += chr(char_val)
            else:
                name3 += '?'
        results[f"xor_byte_{i}"] = name3

    # Méthode 4: Décalage avec différentes valeurs
    for shift_val in range(1, 8):
        name4 = ""
        for value in name_encrypted:
            char_val = value >> shift_val
            if 32 <= char_val <= 126:
                name4 += chr(char_val)
            else:
                name4 += '?'
        results[f"shift_{shift_val}"] = name4

    return results


# Données du binaire
MOVE_ENCRYPTED = "Aq+8"
MOVE_KEY = 19
NAME_ENCRYPTED = [158, 160, 138, 164, 130, 64, 142, 130, 154, 138]

# Déchiffrement du coup
decoded_move, decoded_bytes = xor_decode_move(MOVE_ENCRYPTED, MOVE_KEY)
print(f"Coup déchiffré: {decoded_move}")

# Calcul du mystery_number
mystery_number = int.from_bytes(bytes(decoded_bytes[:4]), byteorder='little', signed=True)
print(f"Mystery number: {mystery_number}")

# Essai de différentes méthodes de déchiffrement
results = decode_name_alternative(NAME_ENCRYPTED, mystery_number)

print("\nDifférentes méthodes de déchiffrement du nom:")
for method, name in results.items():
    clean_name = ''.join(c for c in name if c.isprintable())
    print(f"{method}: '{clean_name}'")
