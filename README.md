# brain-tumor
brain-tumor est le nom de ce projet notre projet d'ESIR2 SI. Ce dépôt contient notre code source et sa documentation.<br>
Nous avons développé une solution intitulée "Visual Gliome" : une application web permettant de prédire les zones cancéreuses d'un cerveau, appelées "gliomes", sur base d'images d'IRM.
## Demo
### En ligne
Testez le par vous même, sur [visualgliome.bdezordo.com](https://visualgliome.bdezordo.com/).
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
### Installation des dépendances (local)
#### Backend
```bash
cd API/
pip install -r requirements.txt 
```
#### Frontend
```bash
cd frontend/
npm install
```
#### IA
Le dossier contient les fichiers qui permettent de construire le modèle d'IA (entraînement). <br>
La prédiction effective de l'application est gérée dans le backend. <br>
Il n'est donc **pas nécessaire d'installer les dépendances de ce dossier si vous souhaitez seulement exécuter l'application**.<br>
## Exécution (local)
Ouvrez votre navigateur sur [```localhost/```](http://localhost/) pour accéder au frontend. Le backend est disponible sur [```localhost:8000/```](http://localhost:8000). La documentation Swagger autogénérée est disponible à [```/docs```](http://localhost:8000/docs).
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

### IA

### VSCode
Si vous utilisez Visual Studio Code, vous pouvez lancer le backend, le frontend et Chrome en 1 seule action (Sélectionner le profil 'All' dans 'Exécuter et Débuguer', puis appuyez sur F5).

## Docker
Cette app peut aussi tourner sur Docker. 
Il suffit d'exécuter ```docker-compose up```. 
Par défaut, cela va chercher l'image du [frontend](https://hub.docker.com/repository/docker/lfiloche/vg_front) et du [backend](https://hub.docker.com/repository/docker/lfiloche/vg_back) stockés sur DockerHub. Il est aussi possible de créer vous même vos images, avec ```docker-compose build```.

## A propos
Dataset utilisé
https://www.kaggle.com/datasets/dschettler8845/brats-2021-task1

## Documentation
Le répertoire éponyme contient les rapports de management, d'architecture et de management également disponibles dans notre drive Google.

## Doctor_account
Cette BDD contient les comptes des docteurs.

## Auteurs
FILOCHE Léo <br>
MORLOT-PINTA Louis <br>
DE ZORDO Benjamin <br>
LEGRAND Quentin <br>
