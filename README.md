# brain-tumor
brain-tumor est le nom de ce projet notre projet d'ESIR2 SI. Ce dépôt contient notre code source et sa documentation.<br>
Nous avons développé une solution intitulée "Visual Gliome" : une application web permettant de prédire les zones cancéreuses d'un cerveau, appelées "gliomes", sur bases d'images d'IRM.
## Demo
### Visualiseur

https://user-images.githubusercontent.com/62034725/230747859-aebeead9-1fa0-4ec5-af31-305cbb68d956.mp4

## Installation 
### Configuration
Assurez-vous que  [Python](https://www.python.org/downloads/) est installé sur votre machine, avec une version <3.11. (Pour le développement, nous avons utilisé les versions 3.9 et 3.10).
### Clone du projet
Le projet est assez lourd (par son historique), nous vous conseillons de ne cloner que la dernière version :
```bash
git clone --depth 1 https://github.com/FenrirWolf4566/brain-tumor.git 
```
### Backend
```bash
cd API/
pip install -r requirements.txt 
```
### Frontend
```bash
cd frontend/
npm install
```
### IA
Le dossier contient les fichiers qui permettent de construire le modèle d'IA. <br>
La prédiction effective de l'application est gérée dans le backend. <br>
Il n'est donc **pas nécessaire d'installer les dépendances de ce dossier si vous souhaitez seulement exécuter l'application**.<br>
//TODO (Un environnement Python est en cours de préparation)
## Execution (en local)
### Backend
```bash
cd API/
uvicorn main:app --reload
```
### Front End
```bash
cd frontend/
npm run start
```

*Note : si vous utilisez Visual Studio Code, vous pouvez lancer le backend, le frontend et Chrome en 1 seule action (Sélectionner le profil 'All' dans 'Exécuter et Débuguer', puis appuyez sur F5).*

### IA
//TODO

## Docker
Cette app peut tourner sur Docker

### Back End
#### Création de l'image
```bash
cd API/
docker build -t visualgliome_back .
```
#### Execution
```bash
docker run --name vg_back -p 80:80 visualgliome_back
```

### Front End
#### Création de l'image
Vous devez indiquer que l'adresse du backend a changé.
Pour cela, modifier public/consts.js, commenter le premier ROOT_URL (dev mode), et décommenter le second (docker mode), pour indiquer l'adresse et le port du backend
```javascript
// In dev mode
//const ROOT_URL = 'http://127.0.0.1:8000/';
// In docker mode
const ROOT_URL = 'http://localhost:80/';
```

```bash
cd frontend/
docker build -t visualgliome_front .
```
#### Execution
```bash
docker run -d --name vg_front -p 3000:3000 visualgliome_front
```
Consulter ensuite [http://localhost:3000/](http://localhost:3000/)


## A propos
Dataset utilisé
https://www.kaggle.com/datasets/dschettler8845/brats-2021-task1


## Auteurs
FILOCHE Léo <br>
MORLOT-PINTA Louis <br>
DE ZORDO Benjamin <br>
LEGRAND Quentin <br>
