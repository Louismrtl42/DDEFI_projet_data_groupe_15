import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

def train_robust_model(train_file):
    # 1. Chargement
    df_train = pd.read_csv(train_file)

    # 2. Préparation
    cols_to_exclude = ['Name', 'Isin', 'YahooTicker', 'Market', 'Price_per_share_2025']
    features = [c for c in df_train.columns if c not in cols_to_exclude]
    target = 'Price_per_share_2025'

    X_train = df_train[features]
    y_train = df_train[target]

    # 3. Création du Pipeline (Normalisation + Ridge)
    # alpha=1.0 est la force de régularisation. Plus il est haut, plus on calme les extrêmes.
    robust_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('ridge', Ridge(alpha=1.0))
    ])

    # 4. Entraînement
    robust_pipeline.fit(X_train, y_train)

    # 5. Sauvegarde
    model_data = {
        'pipeline': robust_pipeline,
        'features': features
    }
    joblib.dump(model_data, 'mon_modele_2.pkl')
    
    print("Modèle Robuste (Scalé + Ridge) sauvegardé sous 'mon_modele_2.pkl'")

# Lancement
train_robust_model('BDD_Etalonnage_80.csv')