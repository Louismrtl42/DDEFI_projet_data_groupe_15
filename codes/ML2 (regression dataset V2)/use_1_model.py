import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, r2_score

def load_and_test_model(test_file):
    # 1. Chargement du modèle sauvegardé
    data = joblib.load('mon_modele_1.pkl')
    model = data['model']
    features = data['features']

    # 2. Chargement de la base de test
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

    print("--- RÉSULTATS DU TEST SUR LES 20% ---")
    print(f"Précision (R²) : {r2:.4f}")
    print(f"Erreur moyenne : {mae:.2f} €")
    print("\nQuelques exemples de prédictions :")
    print(comparaison.head(10))

    # Optionnel : Sauvegarder les résultats du test
    comparaison.to_csv('resultats_test_model_1.csv', index=False)

# Lancement
load_and_test_model('BDD_Test_20.csv')