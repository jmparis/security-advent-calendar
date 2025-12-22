# Analyse
On a donc récupéré un fichier brut, binaire sans doute.
On le passe dans un Linux.
Puis :
```text
file MoroccoChecker
MoroccoChecker.class: compiled Java class data, version 65.0
```

On renomme le fichier `MoroccoChecker` en `MoroccoChecker.class` et on utilise `javap` pour désassembler la classe Java.
```bash
javap -classpath . -c -verbose MoroccoChecker.class
```
