import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

def train_and_save_model(train_file):
    # 1. Chargement de la base d'étalonnage
    df_train = pd.read_csv(train_file)

    # 2. Préparation des données
    cols_to_exclude = ['Name', 'Isin', 'YahooTicker', 'Market', 'Price_per_share_2025']
    features = [c for c in df_train.columns if c not in cols_to_exclude]
    target = 'Price_per_share_2025'

    X_train = df_train[features]
    y_train = df_train[target]

    # 3. Création et entraînement
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 4. Sauvegarde du modèle et de la liste des colonnes
    # (Il est crucial de sauvegarder l'ordre des colonnes pour le test)
    model_data = {
        'model': model,
        'features': features
    }
    joblib.dump(model_data, 'mon_modele_1.pkl')
    
    print("Étape 1 terminée : Modèle entraîné et sauvegardé sous 'mon_modele_1.pkl'")

# Lancement
train_and_save_model('BDD_Etalonnage_80.csv')