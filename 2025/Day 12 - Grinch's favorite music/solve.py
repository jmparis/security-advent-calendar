#!/usr/bin/env python3
"""
Day 12 - Grinch's favorite music - Solution
Lit la tablature colonne par colonne pour extraire le message Base64
"""

import base64


def extract_base64_from_tablature(filename):
    """
    Lit la tablature colonne par colonne pour extraire le Base64
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Trouver le bloc avec le Base64 (lignes 60-64)
    # 4|-----------------sZl---------|
    # 4|---UR------------------Tn0=--|
    # 3|-----------e2V---------------|
    # 3|-Q------------------BX-------|
    # 2|--------W--------------------|

    suspect_block = []
    for i, line in enumerate(lines):
        if any(x in line for x in ['sZl', 'UR', 'Tn0=', 'e2V', 'BX', 'W']) and '|' in line:
            parts = line.split('|')
            if len(parts) >= 2:
                suspect_block.append(parts[1].rstrip('|\n'))

    if not suspect_block or len(suspect_block) < 5:
        # Recherche manuelle
        suspect_block = [
            '-----------------sZl---------',
            '---UR------------------Tn0=--',
            '-----------e2V---------------',
            '-Q------------------BX-------',
            '--------W--------------------'
        ]

    print("Bloc suspect trouvé:")
    for i, line in enumerate(suspect_block):
        print(f"  {i}: {line}")

    # Trouver la longueur maximale
    max_len = max(len(line) for line in suspect_block)

    # Normaliser les lignes à la même longueur
    normalized = [line.ljust(max_len, '-') for line in suspect_block]

    # Lire colonne par colonne
    result = []
    for col in range(max_len):
        for row in range(len(normalized)):
            char = normalized[row][col]
            if char != '-' and char.isalnum() or char in ['=', '+', '/']:
                # Vérifier que ce n'est pas juste une note musicale
                # Les notes musicales sont généralement isolées
                # Le Base64 forme des groupes
                result.append(char)

    base64_str = ''.join(result)
    print(f"\nBase64 extrait (lecture colonne par colonne): {base64_str}")

    # Essayer de décoder
    try:
        decoded = base64.b64decode(base64_str)
        print(f"Décodage réussi: {decoded}")
        try:
            text = decoded.decode('utf-8')
            print(f"Texte décodé: {text}")
            return text
        except:
            print(f"Hex: {decoded.hex()}")
    except Exception as e:
        print(f"Erreur de décodage: {e}")

    # Essayons une autre approche: extraire uniquement les séquences Base64
    print("\n" + "="*60)
    print("Approche alternative: extraction des séquences")

    # Lire les séquences dans l'ordre d'apparition gauche->droite, haut->bas
    sequences = []
    for line in suspect_block:
        # Trouver les séquences de caractères alphanumériques (2+ caractères consécutifs)
        i = 0
        while i < len(line):
            if line[i].isalnum() or line[i] in ['=', '+', '/']:
                seq = line[i]
                j = i + 1
                while j < len(line) and (line[j].isalnum() or line[j] in ['=', '+', '/']):
                    seq += line[j]
                    j += 1
                if len(seq) >= 2:  # Au moins 2 caractères
                    sequences.append((i, seq))
                i = j
            else:
                i += 1

    print("Séquences trouvées (position, texte):")
    for pos, seq in sequences:
        print(f"  Position {pos:2d}: {seq}")

    # Trier par position pour lire de gauche à droite
    sequences.sort(key=lambda x: x[0])

    # Essayer différentes combinaisons
    # En lisant de gauche à droite: UR (pos 3), W (pos 8), e2V (pos 11), sZl (pos 17), Q (pos 1), BX (pos 20), Tn0= (pos 23)
    base64_attempts = [
        ''.join(seq for _, seq in sequences),  # Toutes les séquences
        'URWe2VsZlQBXTn0=',  # Ordre gauche->droite
        'QsZlURe2VBXWTn0=',
        'QWsZle2VURBXTn0=',
        'QURWe2VsZlBXTn0=',  # Q + UR + W + e2V + sZl + BX + Tn0=
        'We2VsZlQBXURTn0=',
    ]

    print("\nTentatives de décodage:")
    for attempt in base64_attempts:
        print(f"\n  Tentative: {attempt}")
        try:
            decoded = base64.b64decode(attempt)
            print(f"    Bytes: {decoded}")
            try:
                text = decoded.decode('utf-8')
                print(f"    UTF-8: {text}")
                if 'ADV{' in text or text.isprintable():
                    print(f"    >>> FLAG POTENTIEL: {text} <<<")
                    return text
            except:
                print(f"    Hex: {decoded.hex()}")
        except Exception as e:
            print(f"    Erreur: {e}")

    return None


if __name__ == "__main__":
    filename = "input.txt"

    print("=" * 60)
    print("Day 12 - Grinch's favorite music")
    print("=" * 60)
    print()

    result = extract_base64_from_tablature(filename)

    if result:
        print("\n" + "=" * 60)
        print(f"SOLUTION: {result}")
        print("=" * 60)

