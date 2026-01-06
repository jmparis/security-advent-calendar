import struct


# Lecture des données exactes du binaire
def extract_name_encrypted_from_binary():
    # Les valeurs NAME_ENCRYPTED dans la section .data
    # À l'offset 0x4020 dans le binaire
    return [158, 160, 138, 164, 130, 64, 142, 130, 154, 138]


def find_correct_fen_position():
    """
    Recherche la position FEN correcte pour la Partie de l'Opéra
    où le coup Rb8+ peut être joué
    """

    # Positions FEN possibles dans la Partie de l'Opéra
    possible_positions = [
        # Position après 8...Rd8 (avant Rxd7)
        "r2qkb1r/ppp2ppp/2n2n2/3pp1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R w KQkq - 0 9",

        # Position après 9.Rxd7 Rxd7 10.Rd1 (avant Qe6)
        "3qkb1r/ppp1rppp/2n2n2/3pp1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R b KQkq - 2 10",

        # Position après 10...Qe6 (avant Bxd7+)
        "4kb1r/ppp1rppp/2n1qn2/3pp1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R w KQkq - 3 11",

        # Position après 11.Bxd7+ Nxd7 (avant Qb8+)
        "4kb1r/ppp1Bppp/2n1qn2/4p3/4P3/3P1N2/PPP2PPP/RN1QK2R b KQkq - 0 11",

        # Position alternative où une tour peut jouer Rb8+
        "r3kb1r/ppp1nppp/2n1q3/3pp1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R w KQkq - 4 12",

        # Position avec tour noire active
        "1r2kb1r/ppp1nppp/2n1q3/3pp1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R b KQkq - 5 12",

        # Position classique de la Partie de l'Opéra (variante)
        "r1bqk2r/pppp1ppp/2n2n2/4p1B1/1bB1P3/3P1N2/PPP2PPP/RN1QK2R b KQkq - 5 6",

        # Position après les premiers coups de la Partie de l'Opéra
        "rnbqkb1r/ppp2ppp/3p1n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 4",

        # Position où les Noirs peuvent jouer Rb8+
        "1rbqkb1r/ppp2ppp/2np1n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R b KQkq - 1 5"
    ]

    return possible_positions


# Données confirmées
MOVE_ENCRYPTED = "Aq+8"
MOVE_KEY = 19
NAME_ENCRYPTED = [158, 160, 138, 164, 130, 64, 142, 130, 154, 138]

# Déchiffrement confirmé
decoded_move = "Rb8+"
decoded_name = "OPERA GAME"

print(f"Coup déchiffré: {decoded_move}")
print(f"Nom déchiffré: {decoded_name}")
print("\nPositions FEN à tester:")

positions = find_correct_fen_position()
for i, fen in enumerate(positions, 1):
    print(f"{i}. {fen}")

# Analyse du mystery number pour d'autres indices
mystery_number = 725115474
print(f"\nMystery number: {mystery_number}")
print(f"En hexadécimal: 0x{mystery_number:08x}")
print(f"En binaire: {bin(mystery_number)}")

# Peut-être que le mystery number encode une position spécifique ?
# Essayons de le décomposer
print(f"\nDécomposition du mystery number:")
print(f"Bytes: {[(mystery_number >> (8 * i)) & 0xFF for i in range(4)]}")
