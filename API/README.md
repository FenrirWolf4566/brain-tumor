# API
Ici se trouve le code source de l'API REST du projet.
Elle permet l'interaction entre le frontend et le modèle de prédiction.
## Installer les dépendances
```pip install -r requirements.txt```
## Executer
```uvicorn main:app --reload```
## Architecture
. <br>
├── requirements.txt : Contient les dépendances nécessaires à la bonne exécution des fichiers python de ce dossier <br>
├── main.py : C'est d'ici que l'API est lancée. Les endpoints sont déclarés à cet endroit. <br>
├── auth.py :  Contient la logique d'authentification <br> 
├── constants.py : Contient les variables relatives à l'authentification<br>
├── model/ : Contient les données du modèle de prédiction<br>
├── niftis/ : Contient des fichiers .nii qui sont utiles pour l'API.<br>
├── predict.py : Contient la logique principale pour la prédiction  du modèle.<br>
├── train_model.py : Contient l'accès au modèle entrainé.<br>
├── variables.py : Contient les variables relatives au modèle d'IA.<br>
├──────Ce qui suit n'est pas encore intégré au fonctionnement général de l'API───────<br>
├── bdd.py : Contient des fonctions d'interaction avec une BDD <br>
├── clients.py : Contient des fonctions d'accès au contenu d'une BDD.<br>
└── mydatabase.py : Contient des fonctions de chargement d'une BDD