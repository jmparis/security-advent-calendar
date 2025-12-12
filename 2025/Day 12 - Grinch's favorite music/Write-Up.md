# Write-Up - Day 12 : Grinch's favorite music

## 🎯 Objectif

Trouver le flag caché dans une partition musicale interceptée entre le Grinch et ses complices.

**Format du flag :** `ADV{something}`

## 📋 Fichiers fournis

- `Challenge.md` : Description du challenge avec lien YouTube
- `input.txt` : Partition de guitare/basse sous forme de tablature

## 🔍 Analyse initiale

### Observation de la partition

Le fichier `input.txt` contient une tablature de guitare/basse classique avec des notes musicales standard (e, G, C, D, a, b, etc.).

En examinant attentivement le fichier, on remarque un bloc suspect aux lignes 60-64 qui contient des caractères inhabituels pour une partition musicale :

```
4|-----------------sZl---------|
4|---UR------------------Tn0=--|
3|-----------e2V---------------|
3|-Q------------------BX-------|
2|--------W--------------------|
```

### Identification du pattern

Ces caractères (`sZl`, `UR`, `Tn0=`, `e2V`, `Q`, `BX`, `W`) ne correspondent pas à des notes musicales standard. La présence du caractère `=` dans `Tn0=` est un fort indicateur de **Base64** (le `=` est utilisé comme padding en Base64).

## 💡 Hypothèse

Le message est encodé en Base64 et dispersé dans la tablature. Il faut extraire ces caractères dans le bon ordre pour reconstituer la chaîne Base64 complète.

## 🛠️ Méthode de résolution

### Étape 1 : Extraction des séquences

En examinant la position des caractères suspects dans chaque ligne :

| Position | Séquence | Ligne (corde) |
|----------|----------|---------------|
| 1        | Q        | 3             |
| 3        | UR       | 4             |
| 8        | W        | 2             |
| 11       | e2V      | 3             |
| 17       | sZl      | 4             |
| 20       | BX       | 3             |
| 23       | Tn0=     | 4             |

### Étape 2 : Lecture de la tablature

Une tablature se lit **colonne par colonne**, de gauche à droite. En appliquant cette logique et en lisant les caractères dans l'ordre des colonnes :

**Colonne par colonne, on obtient :** `Q` → `UR` → `W` → `e2V` → `sZl` → `BX` → `Tn0=`

**Chaîne Base64 reconstituée :** `QURWe2VsZlBXTn0=`

### Étape 3 : Décodage Base64

En décodant la chaîne Base64 :

```python
import base64

encoded = "QURWe2VsZlBXTn0="
decoded = base64.b64decode(encoded)
print(decoded.decode('utf-8'))
```

**Résultat :** `ADV{elfPWN}`

## 🚀 Script de résolution automatique

Un script Python (`solve.py`) a été développé pour automatiser l'extraction et le décodage :

### Fonctionnalités principales

1. **Détection du bloc suspect** : Recherche des lignes contenant des caractères non-musicaux
2. **Extraction colonne par colonne** : Lecture de la tablature selon la convention musicale
3. **Décodage Base64** : Tentative de décodage automatique
4. **Validation du flag** : Vérification du format `ADV{...}`

### Exécution

```bash
python solve.py
```

### Sortie du script

```
============================================================
Day 12 - Grinch's favorite music
============================================================

Bloc suspect trouvé:
  0: -----------------sZl---------
  1: ---UR------------------Tn0=--
  2: -----------e2V---------------
  3: -Q------------------BX-------
  4: --------W--------------------

Base64 extrait (lecture colonne par colonne): QURWe2VsZlBXTn0=
Décodage réussi: b'ADV{elfPWN}'
Texte décodé: ADV{elfPWN}

============================================================
SOLUTION: ADV{elfPWN}
============================================================
```

## 🏆 Solution finale

**Flag :** `ADV{elfPWN}`

## 📚 Points clés à retenir

1. **Stéganographie musicale** : Les données peuvent être cachées dans des formats inattendus comme les partitions musicales
2. **Lecture contextuelle** : Il est important de comprendre comment lire le médium utilisé (ici, une tablature se lit colonne par colonne)
3. **Reconnaissance de patterns** : Le caractère `=` est un indicateur fort de Base64
4. **Encodage Base64** : Un des encodages les plus courants en CTF pour cacher des messages textuels

## 🎵 Analyse du titre

Le flag `elfPWN` fait référence à un "elf" (lutin en anglais) qui a été "pwned" (compromis/hacké dans le jargon de la sécurité informatique), ce qui correspond bien au scénario du challenge où le Grinch prépare une cyberattaque contre Noël.

---

**Difficulté :** ⭐⭐☆☆☆ (Moyenne)  
**Catégorie :** Stéganographie / Encodage  
**Compétences :** Base64, Lecture de tablature, Extraction de données

