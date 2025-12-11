
# Write-Up
On récupère les 2 morceaux de musique, un en _Anglais_, l'autre en _Français_. Bon rapidemment, je me doute qu'ils sont joués à l'envers.

## Audacity
Installation d'Audacity (depuis le Microsoft Store).

- Ouverture du fichier `ADV--French.wav`.
- `Effets` --> `Special` --> `Inverser sens`

Voilà, maintenant, ça joue la chanson à l'endroit (Merci à Sora ?)

## Paroles
Pour se faciliter la vie, on va extraire les paroles de la chanson. Histoire de ne pas réécouter en boucle la musique.

### 1. Utilisation du site [lyrixer.com](https://lyrixer.com/fr)

Texte Extrait
```text
Je, sous-signé le Grinch, vous propose en guise d'énigme quelques savoureuses hémistiches. En jouant cette chanson à l'envers, vous avez eu l'audace de vous aventurer dans mon repère.

Pourquoi venir en aide à ce satané Père Noël ?
Quand vous et moi pourrions faire des étincelles.

Mon intelligence artificielle est redoutable. Ma victoire contre vos amis les elfes est inévitable.

Voici quelques énigmes de cybersécurité, diaboliques et retorses. Tenez-vous prêts, c'est là que ça se corse !

En troisième position, numéro 3, la première lettre d'un logiciel malveillant qui réclame des bitcoins après avoir chiffré toutes vos données.

En deuxième position, numéro 2, la première lettre d'une cellule d'Orange, l'équipe à qui vous pouvez signaler des mails frauduleux ou usurpés.

En sixième position, numéro 6, la première lettre d'un logiciel qui stocke tous vos identifiants et mots de passe dans un coffre-fort sécurisé.

En quatrième position, numéro 4, la première lettre d'un pilier de la cybersécurité, il est associé à la disponibilité et à la confidentialité.

En neuvième position, numéro 9, la première lettre d'un réseau qui permet de naviguer sur internet de façon anonyme, son logo est un oignon violet.

En première position, numéro 1, la première lettre d'une personne de range de niveau 1 ou 2, habilité à délivrer vos certificats PKI sur une clé USB.

En cinquième position, numéro 5, la première lettre d'une technique qui rend du code informatique confus, très difficile à déchiffrer et à analyser.

En huitième position, numéro 8, la première lettre d'un algorithme cryptographique, ce sont Tani Chamir, Henri Bessé et Léonard Ademan qui l'ont créé.

En septième position, numéro 7, la première lettre du prénom du célèbre mathématicien britannique qui de la machine énigma l'abri l'amour triomphé.

Je deviendrai mauvais d'humeur mausade, si d'aventure vous obtenez le flag, tout en majuscule préfixé par ADV, placé entre accolade.
```

### Quelques réponses rapides:
```text
Lettre 1: ?
Lettre 2: ?
Lettre 3: R
Lettre 4: ?
Lettre 5: O
Lettre 6: K
Lettre 7: A
Lettre 8: R
Lettre 9: T
```

Soit : **..R.OKART**


### Avec GPT-5
```text
🔎 Étape par étape
- Numéro 1 : personne de rang niveau 1 ou 2 habilitée à délivrer des certificats PKI → c’est un RA (Registration Authority). Première lettre = R.
- Numéro 2 : cellule d’Orange pour signaler des mails frauduleux → CERT Orange (Computer Emergency Response Team). Première lettre = C.
- Numéro 3 : logiciel malveillant qui réclame des bitcoins après chiffrement → Ransomware. Première lettre = R.
- Numéro 4 : pilier de la cybersécurité avec disponibilité et confidentialité → Intégrité. Première lettre = I.
- Numéro 5 : technique qui rend du code confus → Obfuscation. Première lettre = O.
- Numéro 6 : logiciel qui stocke identifiants/mots de passe → KeePass (ou gestionnaire de mots de passe). Première lettre = K.
- Numéro 7 : mathématicien britannique lié à Enigma → Alan Turing. Première lettre = A.
- Numéro 8 : algorithme cryptographique créé par Rivest, Shamir, Adleman → RSA. Première lettre = R.
- Numéro 9 : réseau anonyme avec logo oignon violet → Tor. Première lettre = T.
🧩 Assemblage des lettres
On place les lettres dans l’ordre des positions données :
1 → R
2 → C
3 → R
4 → I
5 → O
6 → K
7 → A
8 → R
9 → T
👉 Résultat = RCRIOKART
🎉 Flag final
Le challenge précise : tout en majuscule, préfixé par ADV, placé entre accolades.
Donc le flag est :
ADV{RCRIOKART}
```
Bizarre ce flag ADV{RCRIOKART} 🤔
Essai : **ADV{RCRIOKART}** ❌

Tu veux que je t’explique aussi le sens caché du mot obtenu (ça ressemble à "MARIOKART" mais avec un twist cyber) ?


### Avec les deux
Je valide : **..RIOKART**

Tiens Mariokart, c'est pas mal, à essayer !

Essai : **ADV{MARIOKART}** ✅


---