# Projet Neige et Soleil - Django
Ce projet est un client léger réaliser dans le cadre de mon BTS SIO SLAM en tant que projet de fin d'année

## Installation 

### Installer les dependencies

1. Installer python3 IDE depuis le site : https://www.python.org/downloads/.
Si vous êtes sur Windows n'oubliez pas d'ajouter python à PATH. Attention tout le projet est fait sur Python3 
   (Si nécessaire dans vos commandes au lieu de python utilisez python3).
2. Cloner le projet GitHub : git -clone https://github.com/ShanAZIZ/neige_soleil_django
   
3. Installer les dependencies - Mettez vous dans le répertoire du projet et tapez
   la commande suivante 
   
    `pip install -r requirements.txt`
4. Renommer le fichier ".env.example" en ".env" et ajouter les configurations demandées 
   (SECRET_KEY, DEBUG). Ces configurations seront spécifiées ultérieurement
   
### Installer la base de donnée

1. Lancer votre serveur MySQL, et créer une nouvelle base de donnée
2. Configurer le fichier settings.py avec les informations de votre base de donnée (HOST, PORT)
3. Renommez le fichier my.cnf.example en my.cnf et complétez les données nécessaires(user, password)
4. Lancer la commande `python manage.py makemigrations`
5. Puis la commande `python manage.py migrate`
6. Pour créer un administrateur :
   `python manage.py createsuperuser`

## Utilisation 

Pour démarrer votre serveur de développement Django, utilisez la commande `python3 manage.py runserver`

## API

