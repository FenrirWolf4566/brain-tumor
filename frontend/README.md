# frontend
## Installation
Assurez vous d'avoir [npm](https://nodejs.org/en) en ligne de commande d'installé au préalable.
```npm install```
## Exécuter
```npm run start```
## Architecture
Ce projet utilise le framework javascript [Astro](https://astro.build/). <br>
Le dossier ```public``` contient les scripts des librairies externes et les icônes. <br>
Le dossier ```src```contient le code source de l'application. <br>
```pages``` contient le contenu de chaque page de l'application. Chaque nouveau fichier .astro dans ce dossier correspond à une nouvelle page dans l'application. <br>
```layouts``` contient des squelettes de pages. <br>
```components``` contient des composants réutilisables dans chaque page.<br>
```styles```contient les feuilles de styles (écrites en SCSS).
```
. 
├── public/
├── src
│   ├── components/
│   ├── layouts/
│   ├── pages/
│   └── styles/
```
## Docker
Vous pouvez construire l'image du frontend avec l'image suivante.
```docker build -t visualgliome_front .```