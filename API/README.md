# API
Ici se trouve le code source de l'API REST du projet.
Elle permet l'interaction entre le frontend et le modèle de prédiction.
## Installer les dépendances
```pip install -r requirements.txt```
## Executer
```uvicorn main:app --reload```
## Architecture
```
. 
├── requirements.txt : Contient les dépendances nécessaires à la bonne exécution des fichiers python de ce dossier. 
├── main.py : C'est d'ici que l'API est lancée. Les endpoints sont déclarés à cet endroit. 
├── services.py : Contient la logique métier de l'API, avec des fonctions de stockage de fichiers .nii et d'appel de la prédiction. 
├── auth.py :  Contient la logique d'authentification.  
├── constants.py : Contient les variables relatives à l'authentification
├── model/ : Contient les données du modèle de prédiction
├── niftis/ : Contient des fichiers .nii qui sont utiles pour l'API. (exemples, stubs)
├── predict.py : Contient la logique principale pour la prédiction  du modèle.
├── train_model.py : Contient l'accès au modèle entrainé.
├── variables.py : Contient les variables relatives au modèle d'IA.
├── bdd.py : Contient des fonctions d'interaction avec une BDD. 
├── clients.py : Contient des fonctions d'accès au contenu d'une BDD.
└── doctors.db : Base de données contenant des identifiants / mots de passe permettant aux docteurs de s'authentifier.
```

## Docker
Vous pouvez construire l'image du backend avec l'image suivante.
```docker build -t visualgliome_back .```

## Users
Chaque product owner dispose d'un id, nom, mail, mot de passe et peut se connecter

## Tests
Vous pouvez exécuter les différents tests écrits dans le dossier test/ en vous plaçant à la **racine** du projet.
```bash
# Une fois à la racine du projet
pytest --show-progress
``` 
Attention, les tests prennent du temps à être exécutés (environ 4 minutes).
