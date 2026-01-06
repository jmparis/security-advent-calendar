def analyze_mystery_number_deeply():
    mystery_number = 725115474

    print(f"Mystery number: {mystery_number}")
    print(f"En hexadécimal: 0x{mystery_number:08x}")
    print(f"En binaire: {bin(mystery_number)}")

    # Décomposition en bytes (little-endian comme dans le binaire)
    bytes_list = [(mystery_number >> (8 * i)) & 0xFF for i in range(4)]
    print(f"Bytes (little-endian): {bytes_list}")
    print(f"Bytes en hex: {[hex(b) for b in bytes_list]}")
    print(f"Bytes en ASCII: {[chr(b) if 32 <= b <= 126 else '?' for b in bytes_list]}")

    # C'est exactement les bytes de "Rb8+" !
    # 0x52 = 'R', 0x62 = 'b', 0x38 = '8', 0x2B = '+'

    # Peut-être que le mystery number encode une position d'échecs ?
    # Essayons différentes interprétations

    # 1. Comme coordonnées d'échecs (0-63 pour chaque case)
    print(f"\n=== Analyse comme coordonnées d'échecs ===")
    for bits in [6, 8, 16]:
        coords = []
        temp = mystery_number
        while temp > 0:
            coord = temp & ((1 << bits) - 1)
            coords.append(coord)
            temp >>= bits
        print(f"Avec {bits} bits par coordonnée: {coords}")

        # Conversion en notation d'échecs si c'est des coordonnées 0-63
        if bits == 6:
            chess_coords = []
            for coord in coords:
                if 0 <= coord <= 63:
                    file = chr(ord('a') + (coord % 8))
                    rank = str((coord // 8) + 1)
                    chess_coords.append(file + rank)
                else:
                    chess_coords.append("??")
            print(f"Cases d'échecs: {chess_coords}")

    # 2. Comme hash ou checksum
    print(f"\n=== Analyse comme hash ===")
    print(f"Modulo 64: {mystery_number % 64}")
    print(f"Modulo 8: {mystery_number % 8}")
    print(f"Modulo 16: {mystery_number % 16}")

    # 3. Comme timestamp ou date
    print(f"\n=== Analyse temporelle ===")
    import datetime
    try:
        # Comme timestamp Unix
        dt = datetime.datetime.fromtimestamp(mystery_number)
        print(f"Comme timestamp Unix: {dt}")
    except:
        print("Pas un timestamp Unix valide")

    # 4. Recherche de patterns
    print(f"\n=== Recherche de patterns ===")
    hex_str = f"{mystery_number:08x}"
    print(f"Hex string: {hex_str}")

    # Peut-être que c'est lié à la Partie de l'Opéra de 1858 ?
    year_1858 = 1858
    print(f"Relation avec 1858: {mystery_number // year_1858} (quotient)")
    print(f"Relation avec 1858: {mystery_number % year_1858} (reste)")

    # 5. Comme ID de base de données
    print(f"\n=== Comme ID de base de données ===")
    print(f"Pourrait être un ID ChessBase: {mystery_number}")
    print(f"Pourrait être un ID PGN: {mystery_number}")

    # 6. Décomposition factorielle
    print(f"\n=== Factorisation ===")
    n = mystery_number
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    print(f"Facteurs premiers: {factors}")


analyze_mystery_number_deeply()
