import pandas as pd
import numpy as np

def clean_and_merge_databases(corp_file, price_file, output_file):
    # 1. Chargement de la base corporate
    # Utilisation de sep=None pour détecter automatiquement le séparateur
    df_corp = pd.read_csv(corp_file, sep=None, engine='python')

    # --- GESTION DES DOUBLONS ---
    df_corp = df_corp.drop_duplicates(subset=['ISIN'], keep='first')

    # 2. Nettoyage des colonnes financières
    # On cible les colonnes numériques des années 2021 à 2024
    cols_to_fix = [c for c in df_corp.columns if any(year in c for year in ['2021', '2022', '2023', '2024'])]
    for col in cols_to_fix:
        df_corp[col] = df_corp[col].astype(str).str.replace(',', '.')
        df_corp[col] = pd.to_numeric(df_corp[col], errors='coerce')

    # 3. Chargement de l'historique des prix
    df_hist = pd.read_csv(price_file, sep=';')
    df_hist = df_hist.drop_duplicates(subset=['ISIN'], keep='first')

    # 4. Extraction du prix MOYEN (4 dernières semaines de l'année)
    # Cela évite de subir la volatilité d'un seul jour précis
    years = ['2021', '2022', '2023', '2024', '2025']
    price_results = []
    date_cols = [c for c in df_hist.columns if '/' in c]
    
    for _, row in df_hist.iterrows():
        res = {'ISIN': row['ISIN']}
        for year in years:
            # On filtre toutes les colonnes dates correspondant à l'année
            year_cols = [c for c in date_cols if c.endswith(year)]
            if year_cols:
                prices = row[year_cols].dropna()
                if not prices.empty:
                    # On calcule la moyenne des 4 derniers prix disponibles pour l'année
                    # (Ou moins si l'année est en cours comme 2025)
                    last_4_weeks = prices.iloc[-4:] 
                    res[f'Price_per_share_{year}'] = last_4_weeks.mean()
                else:
                    res[f'Price_per_share_{year}'] = np.nan
        price_results.append(res)
    
    df_prices = pd.DataFrame(price_results)

    # 5. Fusion des deux bases
    df_final = pd.merge(df_corp, df_prices, on='ISIN', how='inner')

    # 6. Réorganisation des colonnes
    base_info = ['Name', 'ISIN', 'Yahoo_Ticker', 'Market']
    metrics_list = ['Net_Income', 'FCF', 'Op_Margin', 'ROE', 'Debt_Equity', 
                    'PER', 'ROIC', 'Net_Margin', 'EPS', 'Perf']
    
    final_cols = base_info.copy()
    for year in ['2021', '2022', '2023', '2024']:
        for metric in metrics_list:
            col_name = f"{metric}_{year}"
            if col_name in df_final.columns:
                final_cols.append(col_name)
        # On insère le prix lissé de l'année
        if f'Price_per_share_{year}' in df_final.columns:
            final_cols.append(f'Price_per_share_{year}')

    # Ajout du prix lissé de 2025 à la fin (notre cible de prédiction)
    if 'Price_per_share_2025' in df_final.columns:
        final_cols.append('Price_per_share_2025')

    # Filtrage des colonnes pour ne garder que ce qui existe réellement
    final_cols = [c for c in final_cols if c in df_final.columns]
    df_final = df_final[final_cols]

    # --- NETTOYAGE RADICAL ---
    # On supprime les lignes avec des données manquantes
    df_final = df_final.dropna()

    # Renommage pour la propreté finale
    df_final = df_final.rename(columns={'ISIN': 'Isin', 'Yahoo_Ticker': 'YahooTicker'})

    # 7. Sauvegarde
    df_final.to_csv(output_file, index=False, sep=',')
    
    print("-" * 30)
    print(f"Base de données générée : {output_file}")
    print(f"Nombre d'entreprises (100% complètes) : {len(df_final)}")
    print("Méthode : Prix calculés sur la moyenne des 4 dernières semaines de chaque année.")
    print("-" * 30)

# Lancement
clean_and_merge_databases(
    'BDD V0.csv', 
    'HISTORIQUE_HEBDO_2021_2025.csv', 
    'BDD_Finale.csv'
)