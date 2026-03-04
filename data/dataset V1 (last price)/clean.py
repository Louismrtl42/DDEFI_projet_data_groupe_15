import pandas as pd
import numpy as np

def clean_and_merge_databases(corp_file, price_file, output_file):
    # 1. Chargement de la base corporate
    df_corp = pd.read_csv(corp_file, sep=None, engine='python')

    # --- GESTION DES DOUBLONS ---
    df_corp = df_corp.drop_duplicates(subset=['ISIN'], keep='first')

    # 2. Nettoyage des colonnes financières
    cols_to_fix = [c for c in df_corp.columns if any(year in c for year in ['2021', '2022', '2023', '2024'])]
    for col in cols_to_fix:
        df_corp[col] = df_corp[col].astype(str).str.replace(',', '.')
        df_corp[col] = pd.to_numeric(df_corp[col], errors='coerce')

    # 3. Chargement de l'historique des prix
    df_hist = pd.read_csv(price_file, sep=';')
    df_hist = df_hist.drop_duplicates(subset=['ISIN'], keep='first')

    # 4. Extraction du dernier prix disponible par année
    years = ['2021', '2022', '2023', '2024', '2025']
    price_results = []
    date_cols = [c for c in df_hist.columns if '/' in c]
    
    for _, row in df_hist.iterrows():
        res = {'ISIN': row['ISIN']}
        for year in years:
            year_cols = [c for c in date_cols if c.endswith(year)]
            if year_cols:
                prices = row[year_cols].dropna()
                res[f'Price_per_share_{year}'] = prices.iloc[-1] if not prices.empty else np.nan
        price_results.append(res)
    
    df_prices = pd.DataFrame(price_results)

    # 5. Fusion des deux bases
    df_final = pd.merge(df_corp, df_prices, on='ISIN', how='inner')

    # 6. Réorganisation des colonnes (On définit la structure avant le dropna final)
    base_info = ['Name', 'ISIN', 'Yahoo_Ticker', 'Market']
    metrics_list = ['Net_Income', 'FCF', 'Op_Margin', 'ROE', 'Debt_Equity', 
                    'PER', 'ROIC', 'Net_Margin', 'EPS', 'Perf']
    
    final_cols = base_info.copy()
    for year in ['2021', '2022', '2023', '2024']:
        for metric in metrics_list:
            col_name = f"{metric}_{year}"
            if col_name in df_final.columns:
                final_cols.append(col_name)
        final_cols.append(f'Price_per_share_{year}')

    if 'Price_per_share_2025' in df_final.columns:
        final_cols.append('Price_per_share_2025')

    final_cols = [c for c in final_cols if c in df_final.columns]
    df_final = df_final[final_cols]

    # --- NETTOYAGE RADICAL ---
    # Supprime toute ligne qui contient au moins une valeur manquante (NaN) 
    # dans les colonnes sélectionnées ci-dessus.
    df_final = df_final.dropna()

    # Renommer les colonnes
    df_final = df_final.rename(columns={'ISIN': 'Isin', 'Yahoo_Ticker': 'YahooTicker'})

    # 7. Sauvegarde
    df_final.to_csv(output_file, index=False, sep=',')
    print(f"Base de données générée : {output_file}")
    print(f"Nombre d'entreprises avec 100% de données remplies : {len(df_final)}")

# Lancement
clean_and_merge_databases(
    'BDD V0.csv', 
    'HISTORIQUE_HEBDO_2021_2025.csv', 
    'BDD_Finale.csv'
)