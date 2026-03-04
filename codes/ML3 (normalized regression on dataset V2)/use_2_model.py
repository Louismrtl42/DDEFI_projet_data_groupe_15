import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, r2_score

def load_and_test_robust_model(test_file):
    # 1. Chargement du modèle robuste sauvegardé
    # Ce fichier contient le dictionnaire {'pipeline': robust_pipeline, 'features': features}
    data = joblib.load('mon_modele_2.pkl')
    pipeline = data['pipeline']
    features = data['features']

    # 2. Chargement de la base de test (les 20%)
    df_test = pd.read_csv(test_file)
    
    X_test = df_test[features]
    y_test = df_test['Price_per_share_2025']

    # 3. Prédiction
    # Le pipeline applique automatiquement le StandardScaler avant de passer les données au Ridge
    predictions = pipeline.predict(X_test)

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

    print("--- RÉSULTATS DU TEST (MODÈLE 2 : ROBUSTE) ---")
    print(f"Précision (R²) : {r2:.4f}")
    print(f"Erreur moyenne (MAE) : {mae:.2f} €")
    print("\nQuelques exemples de prédictions avec Ridge + Scaling :")
    print(comparaison.head(10))

    # Sauvegarde des résultats pour analyse
    comparaison.to_csv('resultats_test_model_2.csv', index=False)
    print("\nFichier 'resultats_test_model_2.csv' généré.")

# Lancement
load_and_test_robust_model('BDD_Test_20.csv')