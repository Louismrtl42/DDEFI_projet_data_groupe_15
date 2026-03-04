# Analyse Prédictive du Marché PEA (2021-2025)

Ce projet de Machine Learning vise à prédire le prix des actions éligibles au PEA en s'appuyant sur des indicateurs fondamentaux et des données historiques de marché. Le projet suit une démarche itérative, de la régression linéaire simple à l'implémentation de modèles de gradient boosting (XGBoost) segmentés par secteur.

---

## Structure du Projet

Le dépôt est organisé de manière à refléter l'évolution de notre recherche :

* **`data/`** : Contient les différentes versions du dataset (V0 à V3) et sa [Documentation détaillée](./data/Documentation.md).
* **`codes/`** : Historique des modèles expérimentés (ML1 à ML5).
* **`final_model/`** : Contient le modèle de production (`mon_modele_4.pkl`) et le [Rapport de Performance](./final_model/Performance.md).
* **`deployment/`** : Code source de l'API (FastAPI) et de l'Interface Web (AppWeb).
* **`requirements.txt`** : Liste des dépendances nécessaires pour reproduire l'environnement.

---

## Évolution des Choix Techniques

Notre approche a évolué pour pallier les limites des modèles statistiques classiques :

1.  **ML1 & ML2 (Régression Linéaire)** : Baseline pour tester la corrélation brute. Résultats limités par la volatilité et les écarts de prix entre petites et grosses capitalisations.
2.  **ML3 (Ridge + Normalisation)** : Introduction du `StandardScaler` pour équilibrer les variables et de la régularisation Ridge pour stabiliser les coefficients.
3.  **ML4 & ML5 (XGBoost)** : Passage à une logique non-linéaire. Utilisation du **Gradient Boosting** pour capturer les spécificités sectorielles et les interactions complexes entre indicateurs financiers.

> **Résultat Final** : Le modèle XGBoost entraîné sur le Dataset V3 (Moyenne lissée + Secteurs) offre la meilleure robustesse avec une MAE (Erreur Moyenne) de **33.78 €**.

---

## Installation et Utilisation

### 1. Prérequis
Assurez-vous d'avoir Python 3.9+ installé.

### 2. Installation des dépendances
bash
pip install -r requirements.txt

### 3. Lancement API
cd deployment/API
python api.py

### 4. Lancement AppWeb
cd deployment/AppWeb
Python appweb.py
