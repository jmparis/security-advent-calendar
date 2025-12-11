# Write-Up: HOHOH-OTP

## Explication technique sur l'utilisation d'un TOTP
Très bonne explication sur le protocole et les calculs de TOTP.
[Understanding TOTP Two-Factor Authentication](https://www.hendrik-erz.de/post/understanding-totp-two-factor-authentication-eli5)

Comme suggérer, on va copier tous les snippets de code Python. Et on obtient un vrai petit projet.

## TOTP QR Code decoder
Il existe un [décodeur](https://www.token2.com/site/page/totp-qr-image-decoder) de QR code pour les codes TOTP en ligne.
On va donc l'utiliser pour extraire le secret (séquence de 20 octets) du QR code.
On charge l'image du challenge qui contient un QR code.
![1. Décodage du QR Code.png](images/1. Décodage du QR Code.png)

On récupère le secret : `F5TGYYLHNFZW433UNBSXEZJP`

Après un petit décodage avec [CyberChef](https://cyberchef.org/#recipe=From_Base32('A-Z2-7%3D',true)To_Base32('A-Z2-7%3D'/breakpoint)&input=RjVUR1lZTEhORlpXNDMzVU5CU1hFWkpQ).

Le secret est en fait la chaine de caractères : **/flagisnothere/**


## Chaque seconde compte !
Il est montré que le temps s'est arrêté au 24 décembre 21h25:00 à Rovaniemi, en Finlande.
Cette ville est située à **UTC+2h**.

Il faut donc obtenir le temps en UTC. Le temps UTC est le 24 décembre 19h25:00.
Il faut maintenant [convertir](https://www.epochconverter.com/) ce temps en secondes.
![2. Epoch - Nbre de secondes à Rovaniemi.png](images/2. Epoch - Nbre de secondes à Rovaniemi.png)

On récupère le timestamp : `1766604300`


## Exécution du programme
On lance le projet avec en argument le temps figé du challenge : `main.py --time 2025-12-24 19:25:00 --utc`

`Valid tokens: ['920305', '557605', '201734', '591081', '378247']`
5 codes OTP sont affichés pour gérer une fenêtre de temps sur 2 minutes 30 secondes. Mais le challenge ne le supporte pas.
Seule, la valeur centrale du range obtenu est valide. 

On va donc utiliser le code central obtenu pour s'authentifier : **201734**


## Récupération du flag
Une fois, le code OTP **201734** saisi sur le site, on obtient le flag : **ADV{6P5_15_UN10CK3D!}**
