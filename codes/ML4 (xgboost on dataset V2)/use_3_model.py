import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, r2_score

def load_and_test_xgboost_model(test_file):
    # 1. Chargement du modèle XGBoost sauvegardé
    # On récupère le dictionnaire {'model': model_xgb, 'features': features}
    data = joblib.load('mon_modele_3.pkl')
    model = data['model']
    features = data['features']

    # 2. Chargement de la base de test (les 20%)
    df_test = pd.read_csv(test_file)
    
    X_test = df_test[features]
    y_test = df_test['Price_per_share_2025']

    # 3. Prédiction
    predictions = model.predict(X_test)

    # 4. Évaluation
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    # 5. Création d'un tableau comparatif
    comparaison = pd.DataFrame({
        'Entreprise': df_test['Name'],
        'Prix Réel 2025': y_test.round(2),
        'Prix Prédit 2025': predictions.round(2),
        'Écart (€)': (predictions - y_test).round(2)
    })

    print("--- RÉSULTATS DU TEST (MODÈLE 3 : XGBOOST) ---")
    print(f"Précision (R²) : {r2:.4f}")
    print(f"Erreur moyenne (MAE) : {mae:.2f} €")
    print("\nZoom sur les prédictions XGBoost (Arbres de décision) :")
    print(comparaison.head(10))

    # Sauvegarde des résultats
    comparaison.to_csv('resultats_test_model_3.csv', index=False)
    print("\nFichier 'resultats_test_model_3.csv' généré.")

# Lancement
if __name__ == "__main__":
    load_and_test_xgboost_model('BDD_Test_20.csv')