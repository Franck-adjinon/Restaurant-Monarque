![version](https://img.shields.io/badge/version-1.0.0-green)

# Restaurant Monarque 🍽️

Ce projet est un petit site web de démonstration réalisé avec Django. Il représente le site du **restaurant Monarque**, conçu pour m’exercer à Django et aux bases du développement web.

## 🌟 Fonctionnalités

- Affichage des **chefs du restaurant**
- Présentation des **menus** et **plats offerts**
- Section **blog** avec des articles culinaires publiés par le restaurant
- **Formulaire de contact** pour que les visiteurs puissent écrire au restaurant
- **Abonnement à la newsletter** : les abonnés reçoivent un email à chaque publication d’un nouvel article

⚠️ **Aucune inscription ni authentification** pour les visiteurs.  
Pas de like, de commentaires, ni de comptage des vues pour les articles.

---

## 🛠️ Technologies utilisées

- Python / Django
- HTML / CSS
- Bootstrap 
- SQLite (ou la base de données par défaut de Django)
- Django admin + package unfold pour la gestion interne

---

## 🚀 Lancer le projet en local

```bash
git clone https://github.com/Franck-adjinon/Restaurant-Monarque.git
cd Restaurant-Monarque
python -m venv env
source env/bin/activate  # ou env\Scripts\activate sur Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

---

## 🖼️ Aperçu du site

Accueil :  
![Accueil](https://raw.githubusercontent.com/Franck-adjinon/Restaurant-Monarque/master/monarqueproject/static/docs/1.png)

Menus :  
![Blog](https://raw.githubusercontent.com/Franck-adjinon/Restaurant-Monarque/master/monarqueproject/static/docs/2.png)

Plats :  
![Blog](https://raw.githubusercontent.com/Franck-adjinon/Restaurant-Monarque/master/monarqueproject/static/docs/3.png)

Chefs :  
![Blog](https://raw.githubusercontent.com/Franck-adjinon/Restaurant-Monarque/master/monarqueproject/static/docs/4.png)

Blog :  
![Blog](https://raw.githubusercontent.com/Franck-adjinon/Restaurant-Monarque/master/monarqueproject/static/docs/5.png)

📦 Règles de versionnage
Conventions de commit
Format : <type>(<scope>): <description>

Types autorisés : feat, fix, docs, style, refactor, test, chore

Types expliqués :
feat : nouvelle fonctionnalité

fix : correction de bug

docs : mise à jour de la documentation

style : modification de style ou formatage

refactor : amélioration du code sans ajout de fonctionnalité

test : ajout ou mise à jour de tests

chore : maintenance, mises à jour de dépendances

Exemples :
feat(blog): ajout d’un article

fix(contact): correction de l’envoi d’email

style(menu): amélioration du CSS des boutons

Conventions de branches
Branche principale : main

Branche de développement : develop

Format des branches fonctionnelles : <type>/<description-courte>

Exemples :

feat/ajout-newsletter

fix/form-contact

docs/mise-a-jour-readme

📎 Liens utiles
Repo GitHub : https://github.com/Franck-adjinon/Restaurant-Monarque