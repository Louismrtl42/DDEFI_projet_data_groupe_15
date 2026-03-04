import pandas as pd
import xgboost as xgb
import joblib
from sklearn.preprocessing import LabelEncoder

def train_model_4(train_file):
    # 1. Chargement
    df = pd.read_csv(train_file)

    # 2. Création de la cible (Variation en %)
    # On veut prédire : (P2025 - P2024) / P2024
    y = (df['Price_per_share_2025'] - df['Price_per_share_2024']) / df['Price_per_share_2024']

    # 3. Préparation des caractéristiques (X)
    # On exclut les identifiants et le prix de 2025
    cols_to_exclude = ['Name', 'Isin', 'YahooTicker', 'Market', 'Price_per_share_2025']
    features = [c for c in df.columns if c not in cols_to_exclude]
    X = df[features].copy()

    # 4. Encodage du Secteur (Transformation du texte en nombres)
    # XGBoost a besoin de chiffres. LabelEncoder transforme "Industrials" en 0, 1, 2...
    le = LabelEncoder()
    X['Sector'] = le.fit_transform(X['Sector'].astype(str))

    # 5. Configuration et Entraînement de XGBoost
    model_xgb = xgb.XGBRegressor(
        n_estimators=1000,
        max_depth=6,
        learning_rate=0.03,
        objective='reg:squarederror',
        random_state=42,
        # Importance : le sous-échantillonnage aide à ne pas sur-apprendre
        subsample=0.8,
        colsample_bytree=0.8
    )

    print(f"Entraînement du Modèle 4 (Variation %) sur {len(X)} entreprises...")
    model_xgb.fit(X, y)

    # 6. Sauvegarde (On inclut le LabelEncoder pour le programme de test !)
    model_data = {
        'model': model_xgb,
        'features': features,
        'label_encoder': le
    }
    joblib.dump(model_data, 'mon_modele_4.pkl')
    
    print("-" * 30)
    print("Succès : 'mon_modele_4.pkl' généré.")
    print("Cible : Variation du prix 2024 -> 2025")
    print("-" * 30)

if __name__ == "__main__":
    train_model_4('BDD_Etalonnage_80_V3.csv')