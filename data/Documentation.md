Documentation des Datasets
Ce document détaille la genèse et la structure des données utilisées pour l'entraînement de nos modèles de prédiction boursière.

Dataset V0 : Extraction & Scraping (Source)
Le point de départ est une liste d'entreprises éligibles au PEA (BDD E PEA.csv). Un script de scraping automatisé convertit les codes ISIN en Tickers Yahoo Finance pour extraire deux bases distinctes :


1. BDD V0.csv
C'est la base "Fondamentale". Elle contient l'identité de l'entreprise et ses indicateurs financiers annuels (réels et prévisionnels).
Identifiants : Name, ISIN, Symbol, Market, Currency, Yahoo_Ticker, Sector, Industry.
Indicateurs (2021 à 2025) : Pour chaque année, nous extrayons :
Net_Income (Résultat net), FCF (Flux de trésorerie disponible).
Op_Margin (Marge opérationnelle), Net_Margin.
ROE (Rentabilité des capitaux propres), ROIC (Rentabilité du capital investi).
Debt_Equity (Ratio d'endettement), PER (Price Earnings Ratio), EPS (Bénéfice par action).
Perf (Performance annuelle).


2. HISTORIQUE_HEBDO_2021_2025.csv
C'est la base "Temporelle". Elle contient les prix de clôture hebdomadaires.
Structure : ISIN, Yahoo_Ticker suivis de colonnes datées du 01/01/2021 au 19/12/2025.
Usage : Permet de calculer les prix cibles et les tendances de marché.


Évolution des Datasets d'Entraînement
Chaque itération de dataset (V1 à V3) est scindée en deux fichiers pour garantir l'intégrité de l'évaluation :

80% Étalonnage (Training)
20% Test (Validation)


dataset V1 : Fusion Ponctuelle (Last Price)
Logique : On fusionne les métriques financières de BDD V0 avec le dernier prix connu (la dernière colonne) de l'historique hebdomadaire.
Objectif : Créer une corrélation directe entre les résultats comptables et le prix de marché à un instant T.


dataset V2 : Lissage Temporel (Avg Price)
Logique : Identique au V1, mais au lieu du dernier prix brut, on utilise une moyenne des prix sur les 4 dernières semaines.
Objectif : Lisser la volatilité de court terme et capturer une véritable tendance de fin d'année, moins sensible aux bruits de marché.


dataset V3 : Contextualisation Sectorielle
Logique : Reprend la base V2 en y injectant la colonne Sector pour chaque entreprise.
Objectif : Permettre aux modèles avancés (XGBoost) de segmenter l'apprentissage. Le modèle apprend qu'un ratio financier (ex: PER) n'a pas le même poids selon qu'il s'agit du secteur "Technology" ou "Utilities".