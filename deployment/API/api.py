from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import uvicorn

app = FastAPI()

# Autoriser les appels depuis ton app web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger le modèle 4 et ses composants
model_data = joblib.load('mon_modele_4.pkl')
model = model_data['model']
features_list = model_data['features']
le = model_data['label_encoder']

@app.post("/predict")
async def predict(data: dict):
    try:
        # 1. Créer un DataFrame à partir des données reçues
        df_input = pd.DataFrame([data])
        
        # 2. Sauvegarder le prix 2024 pour le calcul final
        p_2024 = float(data['Price_per_share_2024'])
        
        # 3. Encodage du secteur (gérer si le secteur est inconnu)
        sector_name = str(data['Sector'])
        if sector_name in le.classes_:
            df_input['Sector'] = le.transform([sector_name])[0]
        else:
            df_input['Sector'] = -1  # Valeur par défaut pour inconnu
            
        # 4. S'assurer que les colonnes sont dans le bon ordre
        X = df_input[features_list]
        
        # 5. Prédiction de la variation
        variation = model.predict(X)[0]
        
        # 6. Calcul du prix final
        predicted_price = p_2024 * (1 + variation)
        
        return {
            "status": "success",
            "variation_percent": round(float(variation) * 100, 2),
            "predicted_price_2025": round(float(predicted_price), 3)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)