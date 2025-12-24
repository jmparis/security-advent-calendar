# Write-Up : Santa's SBOM Challenge 🎅

## 📝 Informations sur le challenge
- **Nom :** Santa's Gift Delivery Security
- **Catégorie :** Supply Chain Security / Forensics
- **Niveau :** Beginner
- **Objectif :** Identifier un composant vulnérable dans un SBOM et extraire le flag caché.
- **Format du Flag :** `ADV{ceci_est_un_flag}`

---

## 📖 Énoncé
Le Père Noël utilise un nouveau logiciel pour gérer sa distribution de cadeaux. Cependant, un associé du Grinch (**Father Frost**) a injecté une vulnérabilité dans l'un des composants. Nous disposons du fichier **SBOM** (Software Bill of Materials) au format CycloneDX pour mener l'enquête.

---

## 🔍 Analyse du SBOM

### 1. Identification du composant vulnérable
En analysant le fichier `sbom_santa_challenge.json`, on se rend directement à la section `vulnerabilities` située à la fin du document. On y trouve une entrée explicite :

```json
"vulnerabilities": [
  {
    "bom-ref": "vuln-2025-0005",
    "id": "VEX-2025-0005",
    "description": "Vulnérabilité confirmée affectant uniquement le composant father-frost-strap version 0.1.2.",
    "affects": [
      {
        "ref": "pkg:cargo/father-frost-strap@0.1.2"
      }
    ]
  }
]
```

Le composant corrompu est `father-frost-strap` (version 0.1.2).

### 2. Inspection des métadonnées du composant

On remonte dans la liste des composants (components) pour inspecter les détails de father-frost-strap.
Dans la section properties, une ligne attire l'attention :

```json
{
  "name": "father-frost-strap",
  "version": "0.1.2",
  "properties": [
    {
      "name": "org.santa.metadata",
      "value": "owner=rules;build=2025-11-11T03:03:03Z;base58:KkYWdtT6Nh5epg9sS2w5JAu8pG;internal=1"
    }
  ]
}
```

La valeur contient un secret encodé : `base58:KkYWdtT6Nh5epg9sS2w5JAu8pG`

---

## 🔓 Résolution (Le Flag)
Étape de décodage

La chaîne à traiter est `KkYWdtT6Nh5epg9sS2w5JAu8pG`. L'étiquette base58 nous indique l'algorithme à utiliser.
Cependant, le Base58 possède plusieurs alphabets. Après avoir testé l'alphabet standard (Bitcoin) sans succès,
l'utilisation de l'alphabet Ripple permet de décoder la chaîne correctement.

Outil utilisé : CyberChef

Opération : From Base58

Alphabet : **Ripple**

Résultat : flag=ADV{SBOM4EVER}

---

🚩 Flag Final
**ADV{SBOM4EVER}**

---