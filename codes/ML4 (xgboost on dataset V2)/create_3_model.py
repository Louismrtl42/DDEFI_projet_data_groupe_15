import pandas as pd
import xgboost as xgb
import joblib

def train_xgboost_model(train_file):
    # 1. Chargement de la base d'étalonnage (80%)
    df_train = pd.read_csv(train_file)

    # 2. Préparation des données
    # On garde la même logique d'exclusion pour la cohérence
    cols_to_exclude = ['Name', 'Isin', 'YahooTicker', 'Market', 'Price_per_share_2025']
    features = [c for c in df_train.columns if c not in cols_to_exclude]
    target = 'Price_per_share_2025'

    X_train = df_train[features]
    y_train = df_train[target]

    # 3. Création du modèle XGBoost
    # Paramètres de base pour un Jalon 3 robuste :
    # n_estimators : nombre d'arbres (itération)
    # max_depth : profondeur des arbres (pour éviter de trop apprendre par coeur)
    # learning_rate : vitesse d'apprentissage
    model_xgb = xgb.XGBRegressor(
        n_estimators=1000,
        max_depth=5,
        learning_rate=0.05,
        objective='reg:squarederror',
        random_state=42
    )

    # 4. Entraînement
    print("Entraînement du modèle XGBoost en cours...")
    model_xgb.fit(X_train, y_train)

    # 5. Sauvegarde du modèle et des features
    model_data = {
        'model': model_xgb,
        'features': features
    }
    joblib.dump(model_data, 'mon_modele_3.pkl')
    
    print("-" * 30)
    print("Étape terminée : Modèle XGBoost sauvegardé sous 'mon_modele_3.pkl'")
    print(f"Nombre de variables analysées : {len(features)}")
    print("-" * 30)

# Lancement
if __name__ == "__main__":
    train_xgboost_model('BDD_Etalonnage_80.csv')