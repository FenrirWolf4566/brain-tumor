# brain-tumor
brain-tumor est le nom de notre projet d'ESIR2 SI. Ce dépôt contient notre code source et sa documentation.<br>
Nous avons développé une solution intitulée "Visual Gliome" : une application web permettant de prédire grâce à l'IA les zones cancéreuses d'un cerveau, appelées "gliomes", sur base d'images d'IRM.
## Demo
### En ligne
Testez le par vous même, sur [http://visualgliome.bdezordo.com/](http://visualgliome.bdezordo.com/).
### Wiki & documentation
De nombreuses vidéos sont disponibles sur le [wiki](https://github.com/FenrirWolf4566/brain-tumor/wiki) de ce projet. Elles détaillent l'ensemble des fonctionnalités de l'application.
Vous pouvez aussi lire les fichiers présents dans le dossier documentation du projet. Ils détaillent le déroulement du projet. 
### Visualiseur

https://user-images.githubusercontent.com/62034725/235468097-ab5b96d0-575a-4919-a4a3-90ca13e077f3.mp4

### Analyseur

https://user-images.githubusercontent.com/62034725/235467236-7c909dfa-b444-4e06-be60-580fc94e93eb.mp4


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

### VSCode
Si vous utilisez Visual Studio Code, vous pouvez lancer le backend, le frontend et Chrome en 1 seule action (Sélectionner le profil 'DEV' dans 'Exécuter et Débuguer', puis appuyez sur F5).

## Docker
Cette app peut aussi tourner sur Docker. 
Il suffit d'exécuter ```docker-compose up```. 
Par défaut, cela va chercher l'image du [frontend](https://hub.docker.com/repository/docker/lfiloche/vg_front) et du [backend](https://hub.docker.com/repository/docker/lfiloche/vg_back) stockés sur DockerHub. Il est aussi possible de créer vous même vos images, avec ```docker-compose build```.

## A propos
Les fichiers .nii présents dans ce projet proviennent du dataset suivant. [https://www.kaggle.com/datasets/dschettler8845/brats-2021-task1](https://www.kaggle.com/datasets/dschettler8845/brats-2021-task1) <br>
Le modèle qui a été utilisé pour la prédiction est issu de [https://www.kaggle.com/code/rastislav/3d-mri-brain-tumor-segmentation-u-net](https://www.kaggle.com/code/rastislav/3d-mri-brain-tumor-segmentation-u-net)

## Auteurs
FILOCHE Léo <br>
MORLOT-PINTA Louis <br>
DE ZORDO Benjamin <br>
LEGRAND Quentin <br>
