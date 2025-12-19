# Analyse
On voit un QR code géant en haut à droite de la première image.

## Crop level 1
Un premier crop permet d'isoler ce QR code. On utilise un [analyseur](https://zxing.org/w/decode.jspx) en ligne
pour analyser ce QR Code.

Et on obtient les paroles d'une chanson inspirée de Metallica ! Excellent ! 😁

```text
Say your prayers, little one, Don't you peek, my son, When Christmas has come. Tuck you in, warm within, Keep the belief within, 'Til old Clausman has run.

Sleep with both eyes shut tight, Gripping your blanket close.

Exit light! Enter Christ-mas! Take the reins, We’re off to every child's domain!

Something’s wrong? Shut the blinds, The Elves' best work finds Chimneys of all kinds. Dreams of toys, dreams of cheer, Dreams that last the whole year, Banish all doubt and fear.

Sleep with both eyes shut tight, Gripping your blanket close.

Exit light! Enter Christ-mas! Take the reins, We’re off to every child's domain!
Now, my Elves load the sack, they tie it fast, ... Hope the magic will last, ... If you sleep before I land, ... The best gifts will be at hand! ...

Hush, little baby, don't make a sound, And never mind the toys on the ground. It’s just the reindeer on the roof, Leaving Christmas joy for final proof!
Exit light! Enter Christ-mas! Bag of toys! Exit light! Enter Christ-mas! Take the reins, We’re off to every child's domain!

Hoooooo... Elves! Go! Go! Go!
```

## Crop level 2
Bon, je note aussi qu'il y a une zone Orange 😉 dans la première image de QR Code.
Allez hop, on ressort Paint.Net et on crop cette zone orange.

On utilise à nouveau l'[analyseur](https://zxing.org/w/decode.jspx) de QR Code.
Et on obtient le code TOTP :
```text
otpauth://totp/SANTA%20Co:elf@santa.thenorthpole?secret=IFCFM62TIFHFIQJNNFXC2U3POV2GQLKBNVSXE2LDMEQX2&issuer=SANTA%20Co&algorithm=SHA1&digits=6&period=30
```

Le secret est `IFCFM62TIFHFIQJNNFXC2U3POV2GQLKBNVSXE2LDMEQX2` !
Mais bon, on se rappelle qu'il est généralement encodé en Base32.
On va donc utiliser CyberChef avec la bonne [recette](https://cyberchef.org/#recipe=From_Base32('A-Z2-7%3D',true)&input=SUZDRk02MlRJRkhGSVFKTk5GWEMyVTNQT1YyR1FMS0JOVlNYRTJMRE1FUVgy) pour obtenir le secret en clair.

Flag : **ADV{SANTA-in-South-America!}**

