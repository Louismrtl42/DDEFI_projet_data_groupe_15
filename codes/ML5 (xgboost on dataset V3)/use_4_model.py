import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, r2_score

def load_and_test_model_4(test_file):
    # 1. Chargement du modèle 4 et de ses outils
    # On récupère le modèle, la liste des colonnes et le LabelEncoder pour le secteur
    data = joblib.load('mon_modele_4.pkl')
    model = data['model']
    features = data['features']
    le = data['label_encoder']

    # 2. Chargement de la base de test V3
    df_test = pd.read_csv(test_file)
    
    # Copie pour ne pas modifier l'original pendant l'encodage
    X_test = df_test[features].copy()
    
    # Application du même encodage pour le secteur que lors de l'entraînement
    # On gère les nouveaux secteurs inconnus s'il y en a
    X_test['Sector'] = X_test['Sector'].astype(str).map(
        lambda s: le.transform([s])[0] if s in le.classes_ else -1
    )

    # 3. Prédiction de la VARIATION
    # Le modèle nous donne un chiffre comme 0.05 (pour +5%) ou -0.02 (pour -2%)
    predicted_variations = model.predict(X_test)

    # 4. Conversion de la variation en prix réel (€)
    # Formule : Prix_2024 * (1 + Variation_prédite)
    p_2024 = df_test['Price_per_share_2024']
    y_test_price = df_test['Price_per_share_2025']
    
    predictions_price = p_2024 * (1 + predicted_variations)

    # 5. Évaluation (sur les prix finaux pour comparer avec les modèles 1, 2 et 3)
    mae = mean_absolute_error(y_test_price, predictions_price)
    r2 = r2_score(y_test_price, predictions_price)

    # 6. Création du tableau comparatif
    comparaison = pd.DataFrame({
        'Entreprise': df_test['Name'],
        'Secteur': df_test['Sector'],
        'Prix 2024 (€)': p_2024.round(2),
        'Prix Réel 2025 (€)': y_test_price.round(2),
        'Prix Prédit 2025 (€)': predictions_price.round(2),
        'Variation Prédite (%)': (predicted_variations * 100).round(2),
        'Écart (€)': (predictions_price - y_test_price).round(2)
    })

    print("--- RÉSULTATS DU TEST (MODÈLE 4 : SECTEUR + VARIATION %) ---")
    print(f"Précision (R²) basée sur le prix final : {r2:.4f}")
    print(f"Erreur moyenne (MAE) : {mae:.2f} €")
    print("\nZoom sur les prédictions (Logique de rendement sectoriel) :")
    # On affiche les colonnes principales pour le log
    print(comparaison[['Entreprise', 'Secteur', 'Prix Réel 2025 (€)', 'Prix Prédit 2025 (€)', 'Écart (€)']].head(10))

    # Sauvegarde des résultats
    comparaison.to_csv('resultats_test_model_4.csv', index=False)
    print("\nFichier 'resultats_test_model_4.csv' généré.")

if __name__ == "__main__":
    load_and_test_model_4('BDD_Test_20_V3.csv')