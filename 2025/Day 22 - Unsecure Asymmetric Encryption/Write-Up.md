# Analysis

## Une clé RSA en "bois d'arbre"
La clé RSA du challenge est en fait beaucoup trop petite.

### Clé
```text
-----BEGIN PUBLIC KEY-----
MDswDQYJKoZIhvcNAQEBBQADKgAwJwIgATDOKzp991nXIjXWEm0rCqjTmt6ZfDsh
+Fj39HyGAdcCAwEAAQ==
-----END PUBLIC KEY-----
```

### Vérification de cette clé avec `OpenSSL`
On met la clé dans un fichier `pubkey.pem`.
```text
cat pubkey.pem

-----BEGIN PUBLIC KEY-----
MDswDQYJKoZIhvcNAQEBBQADKgAwJwIgATDOKzp991nXIjXWEm0rCqjTmt6ZfDsh
+Fj39HyGAdcCAwEAAQ==
-----END PUBLIC KEY-----
```

On analyse la clé publique avec `OpenSSL`.
```bash
openssl rsa -pubin -in pubkey.pem -text -noout

Public-Key: (249 bit)
Modulus:
    01:30:ce:2b:3a:7d:f7:59:d7:22:35:d6:12:6d:2b:
    0a:a8:d3:9a:de:99:7c:3b:21:f8:58:f7:f4:7c:86:
    01:d7
Exponent: 65537 (0x10001)
```

## Factorisation du Modulus
```text
Modulus:
    01:30:ce:2b:3a:7d:f7:59:d7:22:35:d6:12:6d:2b:
    0a:a8:d3:9a:de:99:7c:3b:21:f8:58:f7:f4:7c:86:
    01:d7
```
On extrait la chaine hexadécimale du Modulus, en virant les ':' et en collant le tout.
`0130ce2b3a7df759d72235d6126d2b0aa8d39ade997c3b21f858f7f47c8601d7`


Avec CyberChef, on la [convertie](https://gchq.github.io/CyberChef/#recipe=From_Base(16)&input=MDEzMGNlMmIzYTdkZjc1OWQ3MjIzNWQ2MTI2ZDJiMGFhOGQzOWFkZTk5N2MzYjIxZjg1OGY3ZjQ3Yzg2MDFkNw) en décimale.
`538544432877706791637697464048120022166488857246411543807627620220620112343`

### Factorisation
Utilisation de [Factordb.com](https://factordb.com/index.php?query=538544432877706791637697464048120022166488857246411543807627620220620112343) pour factoriser l'entier.

```bash
n = p * q
p = 829964450046321974947
q = 648876506515007420328921808692076639722017679557003069
```


## Reconstituer la clé privée
Une fois p et q trouvés, tu peux reconstruire la clé privée RSA.
- Calcule \varphi (n)=(p-1)(q-1)
- Inverse modulaire de e modulo \varphi (n) :

Utilisation de calc_private_key.py pour calculer la clé privée.

Clé privée = `152999966366327765285109291719748291340139949004606538958849601267979693609`


### Déchiffrer le flag
```text
AO4dwRk2Gv0IAndrXO342riZMiO4qhnqBf9E/PmOwts=
```
C'est du _Base64_
```bash
echo 'AO4dwRk2Gv0IAndrXO342riZMiO4qhnqBf9E/PmOwts=' | base64 -d > cipher.bin
```

Option A – Avec OpenSSL
Tu reconstruis un fichier priv.pem (clé privée complète) à partir de n,e,d,p,q avec un script Python (par exemple en utilisant pycryptodome pour générer un objet RSA, puis l’exporter en PEM), puis :
```bash
openssl rsautl -decrypt -in cipher.bin -inkey priv.pem
```
Tu obtiens quelque chose du genre :
`ADV{...}`


Option B - Avec RsaCtfTool

Projet : **https://github.com/RsaCtfTool/RsaCtfTool**
```bash
RsaCtfTool -n 538544432877706791637697464048120022166488857246411543807627620220620112343 -e 65537 --private --decryptfile ./cipher.bin
```


5. Comment “prouver” à Santa que sa clé est mauvaise
Dans ton explication (ou writeup), tu peux dire :
- La clé publique fournie est une clé RSA au format standard.
- Sa taille (XXX bits) est beaucoup trop faible pour être sécurisée.
- On peut factoriser le modulus n en p et q.
- Grâce à ça, on peut recalculer la clé privée, ce qui ne devrait jamais être possible dans un vrai système RSA correctement dimensionné.
- En utilisant cette clé privée, on déchiffre le message et on retrouve le flag ADV{...}.
Si tu veux, tu peux me coller la sortie exacte de :
openssl rsa -pubin -in pub.pem -text -noout



