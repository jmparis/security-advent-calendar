#!/usr/bin/env python3
"""
Day 12 - Grinch's favorite music
Extrait et décode le message caché dans la partition musicale
"""

import base64
import re


def extract_hidden_message(filename):
    """
    Extrait le message Base64 caché dans la partition
    """
    with open(filename, 'r') as f:
        content = f.read()

    # Rechercher tous les caractères qui ne sont pas des notes musicales typiques
    # Notes musicales: a-G, b (bémol), #, -, |, chiffres de cordes
    # Le Base64 contient: A-Z, a-z, 0-9, +, /, =

    lines = content.split('\n')
    base64_chars = []

    for line in lines:
        # Extraire la partie après le pipe
        if '|' in line:
            parts = line.split('|')
            if len(parts) >= 2:
                notation = parts[1]
                # Chercher des caractères qui ressemblent à du Base64
                # et pas à des notes (eviter e, G, C, D, a, b, c, d)
                for char in notation:
                    # Base64 peut contenir: A-Z, a-z, 0-9, +, /, =
                    # Notes musicales communes: e, G, C, D, a, b, c, d, F
                    # On cherche des caractères inhabituels
                    if char.isalnum() or char in ['+', '/', '=']:
                        # Vérifier si c'est potentiellement du Base64
                        if char in ['U', 'R', 'T', 'n', '0', '2', 'V', 'Q', 'B', 'X', 'W', 's', 'Z', 'l']:
                            base64_chars.append(char)

    # Méthode alternative: chercher les lignes avec des caractères suspects
    print("Contenu brut du fichier autour de la ligne suspecte:\n")
    in_suspect_zone = False
    for i, line in enumerate(lines):
        if 'sZl' in line or 'UR' in line or 'Tn0=' in line or 'e2V' in line or 'BX' in line or 'W-' in line:
            print(f"Ligne {i+1}: {line}")
            in_suspect_zone = True
        elif in_suspect_zone and i < len(lines) - 1:
            print(f"Ligne {i+1}: {line}")
            if line.strip() == '':
                in_suspect_zone = False

    return base64_chars


def extract_base64_from_tablature(filename):
    """
    Extrait le Base64 en lisant la partition ligne par ligne
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Rechercher le bloc suspect
    base64_parts = []

    for i, line in enumerate(lines):
        # Chercher les caractères Base64 dans l'ordre de lecture de la tablature
        if '|' in line:
            parts = line.split('|')
            if len(parts) >= 2:
                notation = parts[1]
                # Extraire uniquement les caractères Base64 (pas les notes ni les tirets)
                # En lisant de gauche à droite
                extracted = re.findall(r'[A-Z][A-Z]|[a-z][0-9][A-Z]|Tn0=|sZl|BX|W', notation)
                if extracted:
                    print(f"Ligne {i+1} ({parts[0]}): {notation.strip()} -> {extracted}")
                    base64_parts.extend(extracted)

    return base64_parts


def manual_extraction(filename):
    """
    Extraction manuelle en lisant la partition comme une tablature
    """
    with open(filename, 'r') as f:
        content = f.read()

    # Trouver le bloc suspect
    lines = content.split('\n')

    # Les lignes contenant du Base64
    suspect_lines = []
    for i, line in enumerate(lines):
        if any(x in line for x in ['sZl', 'UR', 'Tn0=', 'e2V', 'BX', 'W']):
            suspect_lines.append((i, line))

    print("\n=== Lignes suspectes ===")
    for i, line in suspect_lines:
        print(f"{i+1}: {line}")

    # Extraire manuellement le Base64 en lisant de gauche à droite
    # Dans l'ordre des cordes (4, 4, 3, 3, 2 de haut en bas)
    print("\n=== Extraction manuelle ===")

    # Ligne par ligne, on lit les caractères Base64
    result = ""

    # On lit les 5 lignes dans l'ordre de la partition
    # 4|-----------------sZl---------|
    # 4|---UR------------------Tn0=--|
    # 3|-----------e2V---------------|
    # 3|-Q------------------BX-------|
    # 2|--------W--------------------|

    # En lisant de gauche à droite, position par position:
    # Position 0-2: ---
    # Position 3-4: UR (ligne 2)
    # Position 8-9: W (ligne 5)
    # Position 11-13: e2V (ligne 3)
    # Position 17-18: sZl (ligne 1)
    # Position 19-20: Q (ligne 4)
    # Position 22-23: BX (ligne 4)
    # Position 24-27: Tn0= (ligne 2)

    # Essayons différentes lectures
    attempts = [
        "URWe2VsZlQBXTn0=",  # lecture gauche à droite
        "sZlURe2VQBXWTn0=",  # autre ordre
        "We2VsZlQBXURTn0=",  # encore autre
        "sZlURTn0=e2VQBXW",  # inversé
    ]

    print("\nTentatives de décodage:")
    for attempt in attempts:
        print(f"\nTentative: {attempt}")
        try:
            decoded = base64.b64decode(attempt)
            print(f"  Décodé (bytes): {decoded}")
            try:
                text = decoded.decode('utf-8')
                print(f"  Décodé (UTF-8): {text}")
            except:
                print(f"  Décodé (hex): {decoded.hex()}")
        except Exception as e:
            print(f"  Erreur: {e}")


if __name__ == "__main__":
    filename = "input.txt"

    print("=" * 60)
    print("Day 12 - Grinch's favorite music - Décodage")
    print("=" * 60)

    # Méthode 1: Extraction automatique
    print("\n[Méthode 1] Extraction automatique:")
    chars = extract_hidden_message(filename)
    print(f"\nCaractères Base64 trouvés: {''.join(chars)}")

    # Méthode 2: Extraction par regex
    print("\n" + "=" * 60)
    print("[Méthode 2] Extraction par regex:")
    parts = extract_base64_from_tablature(filename)
    print(f"\nParties trouvées: {parts}")

    # Méthode 3: Extraction manuelle
    print("\n" + "=" * 60)
    print("[Méthode 3] Extraction manuelle:")
    manual_extraction(filename)

