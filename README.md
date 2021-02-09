# Projet Neige et Soleil - Django
Ce projet est un client leger réaliser dans le cadre de mon BTS SIO SLAM en tant que projet de fin d'année

### Page d'accueil 
La page d'accueil, page sur laquelle on arrive lors de l'ouverture du projet, est une page qui permet de rediriger
vers une page d'inscription ou un page de connexion

### Inscriptions et connexions
superuser : admin_ppe

mot de passe : 

Pour l'inscription et la connexion, nous utiliserons le systeme d'authentification fournis par le framework Django. Le système fournis une table users,
une table groups, et une table permissions. On utilisera pour l'instant uniquement la table users. 

Le systeme comporte aussi des decorators (python : ) pour permettre d'identifier les vues que les utilisateur non authentifiés n'ont 
pas le droits de voir