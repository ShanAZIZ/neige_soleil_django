# Projet Neige et Soleil - Django
Ce projet est un client léger réaliser dans le cadre de mon BTS SIO SLAM en tant que projet de fin d'année

## Installation 

### Installer le projet en developpement

1. Installer python3 IDE depuis le site : https://www.python.org/downloads/.
Si vous êtes sur Windows n'oubliez pas d'ajouter python à PATH. Attention tout le projet est fait sur Python3 
   (Si nécessaire dans vos commandes au lieu de python utilisez python3). 
   Si vous le souhaitez vous pouvez créer un Venv python et effectuer les manipulations avec .
2. Cloner le projet GitHub : git -clone https://github.com/ShanAZIZ/neige_soleil_django
   
3. Installer les dependencies - Mettez vous dans le répertoire du projet et tapez
   la commande suivante 
   
    `pip install -r requirements.txt`
   
4. Renommer le fichier ".env.example" en ".env" et ajouter les configurations demandées 
   (SECRET_KEY, DEBUG). Ces configurations seront spécifiées ultérieurement
   

5. Dans le fichier neige_soleil_django/settings/developement.py remplacez les informations de la base de donnée
par la base que vous souhaitez utiliser.
   

## Utilisation 

Pour démarrer votre serveur de développement Django, utilisez la commande `python3 manage.py runserver`

## API

