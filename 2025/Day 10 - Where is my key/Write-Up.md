# Analyse et déchiffrement du fichier oliver_list.enc

Une version immédiate :
```bash
openssl aes-256-cbc -d -pbkdf2 -iter 100000 -k "grinch_eggnog2025" -in oliver_list.enc -out oliver_list.txt
```