# Système de Recommandation - MovieHub

## Description du projet

MovieHub est une application web de recommandation de films développée avec Streamlit. Le système utilise l'algorithme de similarité cosinus pour analyser les caractéristiques des films (genres et tags) et suggérer des films similaires à celui sélectionné par l'utilisateur.

L'application s'appuie sur le dataset MovieLens 32M pour les données de films et les évaluations, et utilise l'API TMDB pour récupérer les informations complémentaires (affiches, synopsis, dates de sortie, notes).

**État du projet** : En cours de développement

## Fonctionnalités principales

- Sélection d'un film dans une base de 1000 films populaires
- Recommandation de films similaires basée sur les genres et les tags
- Filtrage des résultats par genre
- Filtrage par note minimale
- Affichage des synopsis (optionnel)
- Interface inspirée de Netflix avec design dark mode
- Récupération d'informations enrichies via l'API TMDB

## Prérequis

Avant de commencer, vous devez installer :

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

1. Clonez le repository

```bash
git clone https://github.com/hervoz/systeme-de-recommandation.git
cd systeme-de-recommandation
```

2. Créez un environnement virtuel (recommandé)

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. Installez les dépendances

```bash
pip install -r requirements.txt
```

4. Configurez votre clé API TMDB

Créez un fichier `.streamlit/secrets.toml` à la racine du projet :

```toml
[tmdb]
api_key = "VOTRE_CLE_TMDB_ICI"
```

Vous pouvez obtenir une clé API gratuitement sur https://www.themoviedb.org/settings/api

5. Mettez à jour le chemin des données

Dans `recommender.py`, modifiez la variable `DATA_PATH` pour pointer vers le dossier contenant les fichiers MovieLens 32M :

```python
DATA_PATH = "C:/Votre/Chemin/Vers/ml-32m/"
```

## Dépendances

- **streamlit** : Framework web pour l'interface utilisateur
- **pandas** : Manipulation et analyse des données
- **scikit-learn** : Vectorisation TF-IDF et calcul de similarité cosinus
- **scipy** : Calculs scientifiques
- **requests** : Requêtes HTTP pour l'API TMDB

## Structure du projet

- `app.py` : Application Streamlit principale
- `recommender.py` : Logique du système de recommandation
- `tmdb_client.py` : Client pour interroger l'API TMDB
- `requirements.txt` : Liste des dépendances Python
- `secrets.toml` : Configuration de l'API TMDB

## Utilisation

1. Lancez l'application

```bash
streamlit run app.py
```

2. Ouvrez votre navigateur à l'adresse affichée (généralement http://localhost:8501)

3. Utilisez l'interface pour :
   - Sélectionner un film de référence
   - Ajuster le nombre de recommandations (5 à 20)
   - Filtrer par genre et note minimale
   - Afficher ou masquer les synopsis

4. Cliquez sur le bouton "Recommander" pour voir les résultats

## Algorithme de recommandation

Le système utilise la similarité cosinus sur une matrice TF-IDF construite à partir des genres et tags des films. Les étapes sont :

1. Chargement et prétraitement des données MovieLens
2. Filtrage des 1000 films les plus populaires (minimum 100 évaluations)
3. Construction d'une matrice TF-IDF avec genres et tags
4. Calcul de la similarité cosinus entre tous les films
5. Retour des N films les plus similaires au film sélectionné
6. Application des filtres utilisateur (genre, note)

## Dataset

Le projet utilise le dataset MovieLens 32M qui contient :

- Movies : Titre et genres des films
- Ratings : Évaluations utilisateurs
- Tags : Tags associés aux films
- Links : Correspondance avec TMDB

Télécharger le dataset : https://grouplens.org/datasets/movielens/latest/

## Étapes futures

- Implémentation d'autres algorithmes de recommandation (filtrage collaboratif)
- Optimisation des performances pour l'ensemble complet du dataset
- Ajout d'un système de cache amélioré
- Déploiement sur une plateforme cloud
- Interface pour ajouter des films favoris et générer des recommandations personnalisées

## Limitations actuelles

- Limité à 1000 films populaires (pour des raisons de performance)
- Nécessite un fichier de données local volumineux
- L'API TMDB est appelée en temps réel (peut être lent)

## Contributeurs

Hervoz

## Licence

À définir

## Contact et support

Pour toute question ou suggestion, ouvrez une issue sur le repository.
