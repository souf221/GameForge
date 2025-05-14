# GameForge - Générateur de jeux vidéo par IA

Une plateforme web Django permettant aux utilisateurs de créer des concepts de jeux vidéo originaux à l'aide de modèles d'intelligence artificielle.

## Fonctionnalités

- Génération d'univers de jeu cohérent
- Création d'histoires immersives
- Conception de personnages et lieux
- Génération d'illustrations conceptuelles
- Sauvegarde et partage des concepts

## Installation

1. Cloner le dépôt
2. Créer un environnement virtuel : `python -m venv env`
3. Activer l'environnement : `env\Scripts\activate` (Windows) ou `source env/bin/activate` (macOS/Linux)
4. Installer les dépendances : `pip install -r requirements.txt`
5. Configurer le fichier .env (voir .env.example)
6. Appliquer les migrations : `python manage.py migrate`
7. Lancer le serveur : `python manage.py runserver`