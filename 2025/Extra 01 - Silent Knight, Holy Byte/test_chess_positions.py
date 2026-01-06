import requests
import json
from itertools import product


def extract_data_from_binary():
    """Extrait les données exactes du binaire"""
    # Données extraites du binaire
    MOVE_ENCRYPTED = "Aq+8"  # Dans .rodata
    MOVE_KEY = 19

    # NAME_ENCRYPTED dans .data - valeurs exactes du binaire
    # À l'offset 0x4020 dans la section .data
    NAME_ENCRYPTED = [158, 160, 138, 164, 130, 64, 142, 130, 154, 138]

    return MOVE_ENCRYPTED, MOVE_KEY, NAME_ENCRYPTED


def xor_decode_move(encrypted_move, key):
    """Déchiffre le coup avec XOR"""
    decoded = ""
    decoded_bytes = []
    for char in encrypted_move:
        decoded_char = chr(ord(char) ^ key)
        decoded += decoded_char
        decoded_bytes.append(ord(char) ^ key)
    return decoded, decoded_bytes


def decode_name(name_encrypted, shift):
    """Déchiffre le nom avec décalage de bits"""
    decoded_name = ""
    for value in name_encrypted:
        if shift == 0:
            decoded_name += chr(value)
        else:
            decoded_name += chr(value >> shift)
    return decoded_name


def generate_possible_fens():
    """Génère toutes les positions FEN possibles pour la Partie de l'Opéra"""
    positions = [
        # POSITION FINALE de la Partie de l'Opéra - après 17.Rd8# (mat)
        "1n1Rkb1r/p4ppp/4q3/4p1B1/4P3/8/PPP2PPP/2K5 b k - 1 17",

        # Position avant le mat final (après 16...Nxb8, avant 17.Rd8#)
        "1n2kb1r/p4ppp/4q3/4p1B1/4P3/8/PPP2PPP/2KR4 w k - 0 17",

        # Position après 16.Qb8+ (avant 16...Nxb8)
        "1Q2kb1r/p4ppp/2n1q3/4p1B1/4P3/8/PPP2PPP/2KR4 b k - 5 16",

        # Position avant 16.Qb8+ (après 15...Qe6)
        "4kb1r/p4ppp/2n1q3/4p1B1/4P3/8/PPP2PPP/2KRQ3 w k - 4 16",

        # Positions classiques de la Partie de l'Opéra
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "rnbqkbnr/pppp1ppp/4pn2/8/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 1 3",
        "rnbqkbnr/pppp1ppp/4pn2/8/2B1P3/3P4/PPP2PPP/RNBQK1NR b KQkq - 0 3",
        "r1bqkbnr/pppp1ppp/2n1pn2/8/2B1P3/3P4/PPP2PPP/RNBQK1NR w KQkq - 2 4",
        "r1bqkbnr/pppp1ppp/2n1pn2/8/2B1P3/3P1N2/PPP2PPP/RNBQK2R b KQkq - 3 4",
        "r1bqk1nr/pppp1ppp/2n1pn2/8/1bB1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 4 5",
        "r1bqk1nr/pppp1ppp/2n1pn2/8/1bB1P3/3P1N2/PPP2PPP/RNBQ1RK1 b kq - 5 5",
        "r1bqk2r/pppp1ppp/2n1pn2/8/1bB1P3/3P1N2/PPP2PPP/RNBQ1RK1 w kq - 6 6",
        "r1bqk2r/pppp1ppp/2n2n2/4p3/1bB1P3/3P1N2/PPP2PPP/RNBQ1RK1 b kq - 0 6",
        "r1bqk2r/pppp1ppp/2n2n2/4p1B1/2B1P3/3P1N2/PPP2PPP/RN1Q1RK1 w kq - 1 7",
        "r1bqk2r/pppp1ppp/2n2n2/4p1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R b KQkq - 1 7",
        "r2qk2r/ppppbppp/2n2n2/4p1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R w KQkq - 2 8",
        "r2qk2r/ppppbppp/2n2n2/4p1B1/2B1P3/3P1N2/PPP2PPP/RN1Q1RK1 b kq - 3 8",
        "r2q1rk1/ppppbppp/2n2n2/4p1B1/2B1P3/3P1N2/PPP2PPP/RN1Q1RK1 w - - 4 9",

        # Positions où Rb8+ peut être joué
        "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R b KQkq - 0 4",
        "1rbqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 1 4",
        "r1bqk2r/pppp1ppp/2n2n2/4p1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R b KQkq - 0 5",
        "1rbqk2r/pppp1ppp/2n2n2/4p1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R w KQkq - 1 5",
        "r1bqkb1r/ppp1pppp/2np1n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R b KQkq - 2 4",
        "1rbqkb1r/ppp1pppp/2np1n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 3 4",

        # Positions finales de la Partie de l'Opéra
        "r2qk2r/ppp1bppp/2n2n2/3pp1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R w KQkq - 0 9",
        "r2qk2r/ppp1bppp/2n2n2/3pp1B1/2B1P3/3P1N2/PPP2PPP/RN1Q1RK1 b kq - 1 9",
        "r2q1rk1/ppp1bppp/2n2n2/3pp1B1/2B1P3/3P1N2/PPP2PPP/RN1Q1RK1 w - - 2 10",

        # Variantes avec tour active
        "r1bqk2r/pppp1ppp/2n2n2/4p1B1/1bB1P3/3P1N2/PPP2PPP/RN1QK2R b KQkq - 5 6",
        "1rbqk2r/pppp1ppp/2n2n2/4p1B1/1bB1P3/3P1N2/PPP2PPP/RN1QK2R w KQkq - 6 6",
        "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/2NP1N2/PPP2PPP/R1BQK2R b KQkq - 0 6",
        "1rbqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/2NP1N2/PPP2PPP/R1BQK2R w KQkq - 1 6",
    ]

    return positions


def test_fen_position(fen, move, name, url):
    """Teste une position FEN avec le vérificateur"""
    try:
        # Préparer les données pour la requête JSON
        data = {
            'fen': fen
        }

        # Envoyer la requête POST en JSON vers l'endpoint /verify
        verify_url = url.rstrip('/') + '/verify'
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(verify_url, json=data, headers=headers, timeout=10)

        # Vérifier la réponse
        if response.status_code == 200:
            try:
                json_response = response.json()
                if json_response.get('result') == 'ok':
                    return True, json_response
                else:
                    return False, f"Incorrect: {json_response.get('message', json_response)}"
            except json.JSONDecodeError:
                return False, f"Invalid JSON response: {response.text[:200]}..."
        else:
            return False, f"HTTP {response.status_code}: {response.text[:100]}..."

    except requests.exceptions.RequestException as e:
        return False, f"Request error: {str(e)}"


def main():
    """Fonction principale"""
    print("=== Analyse du binaire chess_game ===")

    # Extraction des données
    MOVE_ENCRYPTED, MOVE_KEY, NAME_ENCRYPTED = extract_data_from_binary()

    # Déchiffrement du coup
    decoded_move, decoded_bytes = xor_decode_move(MOVE_ENCRYPTED, MOVE_KEY)
    print(f"Coup déchiffré: {decoded_move}")

    # Calcul du mystery number
    mystery_number = int.from_bytes(bytes(decoded_bytes), byteorder='little', signed=True)
    print(f"Mystery number: {mystery_number}")

    # Déchiffrement du nom (shift = 1 donne "OPERA GAME")
    decoded_name = decode_name(NAME_ENCRYPTED, 1)
    print(f"Nom déchiffré: {decoded_name}")

    print(f"\n=== Test automatique des positions FEN ===")

    # URL du vérificateur
    url = "https://advent.osecexperts.com/web/SmooEgr5oa2fcrtx4oCaAU3nxF3miP9k/"

    # Génération des positions FEN
    positions = generate_possible_fens()

    print(f"Test de {len(positions)} positions FEN...")
    print(f"Coup: {decoded_move}")
    print(f"Nom: {decoded_name}")
    print(f"URL: {url}")
    print("-" * 80)

    # Test de chaque position
    for i, fen in enumerate(positions, 1):
        print(f"Test {i:2d}/{len(positions)}: {fen[:50]}...")

        success, response = test_fen_position(fen, decoded_move, decoded_name, url)

        if success:
            print(f"🎉 SUCCÈS ! Position FEN trouvée !")
            print(f"FEN: {fen}")
            print(f"Réponse: {response}")
            break
        else:
            print(f"❌ Échec: {response[:100]}...")

    else:
        print("\n❌ Aucune position FEN n'a fonctionné.")
        print("Essayons avec des variantes du nom...")

        # Test avec différentes variantes du nom
        name_variants = [
            "OPERA GAME",
            "Opera Game",
            "opera game",
            "OPERA",
            "Opera",
            "MORPHY",
            "Morphy",
            "PAUL MORPHY",
            "Paul Morphy"
        ]

        # Test avec la première position et différents noms
        test_fen = positions[0]
        for name_variant in name_variants:
            print(f"Test avec nom: '{name_variant}'")
            success, response = test_fen_position(test_fen, decoded_move, name_variant, url)
            if success:
                print(f"🎉 SUCCÈS avec le nom '{name_variant}' !")
                print(f"Réponse: {response}")
                break
        else:
            print("❌ Aucune variante du nom n'a fonctionné.")


if __name__ == "__main__":
    main()
