## 1. Analyse des données du passeport
D'après le visuel, nous avons :
Numéro de passeport : 12304264 (8 caractères)

Nationalité : `NPR`

Date de naissance : 25 DEC 1955 →→ 551225

Sexe : `M`

Date d'expiration : 22 JAN 2034 →→ 340122

---

## 2. Comprendre les champs (Fields) de l'interface
L'interface de scan montre trois champs avec des longueurs spécifiques qui correspondent exactement aux données :
- Field 1 (8 chars) : `12304264` (Le numéro de passeport)
- Field 2 (9 chars) : `NPR551225` (Nationalité + Date de naissance)
- Field 3 (7 chars) : `M340122` (Sexe + Date d'expiration)

---

## 3. La règle de calcul du "Check Digit" (Chiffre de contrôle)
L'énoncé précise que le calcul diffère du standard :
- On utilise toute la zone (lettres incluses), pas seulement les chiffres.
- Poids (weights) classiques : 7, 3, 1 (répétés).
- Valeurs : < = 0, 0-9 = 0-9, A-Z = 10-35.
- Calcul : Somme des produits(mod10). Somme des produits(mod10).

Calculons les chiffres de contrôle pour chaque bloc (ce que l'interface appelle "Verifier") :

### Bloc 1 (Field 1) : 12304264
- (1×7) + (2×3) + (3×1) + (0×7) + (4×3) + (2×1) + (6×7) + (4×3)
- = 7 + 6 + 3 + 0 + 12 + 2 + 42 + 12 = 84
- 84(mod 10) = `4`

### Bloc 2 (Field 2) : NPR551225
- N(23)×7 + P(25)×3 + R(27)×1 + 5×7 + 5×3 + 1×1 + 2×7 + 2×3 + 5×1
- = 161 + 75 + 27 + 35 + 15 + 1 + 14 + 6 + 5 = 339
- 339(mod 10) = `9`

### Bloc 3 (Field 3) : M340122
- M(22)×7 + 3×3 + 4×1 + 0×7 + 1×3 + 2×1 + 2×7
- = 154 + 9 + 4 + 0 + 3 + 2 + 14 = 186
- 186(mod 10) = `6`

---

## 4. Reconstitution de la ligne 2 (MRZ Line 2)
Une ligne MRZ de passeport fait 44 caractères. Elle se compose normalement ainsi :

_[N° Passeport + Check][Nationalité][Date Naissance + Check][Sexe][Date Expire + Check][Données Optionnelles + Check][Check Global]_

En suivant la structure du challenge et les indices :
1. N° Passeport (9 chars avec filler) : 12304264<
2. Check Bloc 1 : 4
3. Nationalité (3 chars) : NPR
4. Date Naissance (6 chars) : 551225
5. Check Bloc 2 : 9
6. Sexe (1 char) : M
7. Date Expire (6 chars) : 340122
8. Check Bloc 3 : 6
9. Personal number / Filler (14 chars) : <<<<<<<<<<<<<<
10. Check Personal : Souvent 0 pour des chevrons.
11. Check Global (Composite Check Digit) : C'est le calcul sur toute la ligne.

---
