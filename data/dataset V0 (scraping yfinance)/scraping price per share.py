import pandas as pd
import yfinance as yf
import time
from datetime import datetime

def get_ticker_from_isin(isin):
    try:
        data = yf.Search(isin, max_results=1).quotes
        if data: return data[0]['symbol']
    except: return None
    return None

def build_weekly_history(input_file, output_file):
    # 1. Charger la liste source
    df_pea = pd.read_csv(input_file)
    
    # 2. Générer la liste des dates (tous les vendredis de 2021 à fin 2025)
    # On utilise 'W-FRI' pour avoir une donnée par semaine (le vendredi)
    date_range = pd.date_range(start='2021-01-01', end='2025-12-31', freq='W-FRI')
    date_columns = [d.strftime('%d/%m/%Y') for d in date_range]
    
    final_rows = []

    print(f"Extraction de l'historique pour {len(df_pea)} entreprises...")

    for _, row in df_pea.iterrows():
        isin = row['ISIN']
        ticker_symbol = get_ticker_from_isin(isin)
        
        if not ticker_symbol:
            print(f"Ticker non trouvé pour {isin}")
            continue
            
        print(f"Récupération : {ticker_symbol}...")
        
        try:
            tk = yf.Ticker(ticker_symbol)
            # Récupération de l'historique max
            hist = tk.history(start="2021-01-01", end="2026-01-01", interval="1wk")
            
            # Créer la ligne de base
            company_row = {
                'ISIN': isin,
                'Yahoo_Ticker': ticker_symbol
            }
            
            # Mapper les prix sur nos colonnes de dates
            for date_obj in date_range:
                date_str = date_obj.strftime('%d/%m/%Y')
                # On cherche la date la plus proche dans l'index de yfinance
                # car les jours fériés peuvent décaler les dates
                try:
                    # On prend le prix de clôture à la date ou juste avant
                    price = hist.asof(date_obj)['Close']
                    company_row[date_str] = round(price, 3) if pd.notnull(price) else ""
                except:
                    company_row[date_str] = ""
            
            final_rows.append(company_row)
            
        except Exception as e:
            print(f"Erreur sur {ticker_symbol}: {e}")
        
        time.sleep(0.5)

    # 3. Création du DataFrame final
    df_final = pd.DataFrame(final_rows)
    
    # Remplacement des points par des virgules pour coller à ton format cible
    df_final = df_final.applymap(lambda x: str(x).replace('.', ',') if isinstance(x, (float, int)) else x)

    # Sauvegarde avec le point-virgule comme séparateur (comme dans ton exemple)
    df_final.to_csv(output_file, index=False, sep=';', encoding='utf-8')
    print(f"Fichier historique sauvegardé : {output_file}")

# Lancement
build_weekly_history('BDD E PEA.csv', 'HISTORIQUE_HEBDO_2021_2025.csv')