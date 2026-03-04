import pandas as pd
import yfinance as yf
import time

def get_ticker_from_isin(isin):

    try:
        # On utilise la recherche de yfinance
        data = yf.Search(isin, max_results=1).quotes
        if data:
            return data[0]['symbol']
    except:
        return None
    return None

def build_v0_database(input_file, output_file):
    # 1. Charger la liste PEA
    df_pea = pd.read_csv(input_file)
    final_data = []

    print(f"Début de l'extraction pour {len(df_pea)} entreprises...")

    for _, row in df_pea.iterrows():
        isin = row['ISIN']
        name = row['Name']
        
        # Trouver le ticker
        ticker_symbol = get_ticker_from_isin(isin)
        if not ticker_symbol:
            print(f"Ticker non trouvé pour {name} ({isin})")
            continue
            
        print(f"Traitement de {name} ({ticker_symbol})...")
        tk = yf.Ticker(ticker_symbol)
        
        # Initialiser le dictionnaire de la ligne
        company_dict = {
            'Name': name,
            'ISIN': isin,
            'Symbol': ticker_symbol.split('.')[0],
            'Market': row['Market'],
            'Currency': row['Currency'],
            'Yahoo_Ticker': ticker_symbol,
            'Sector': row['Sector'],
            'Industry': row['Industry']
        }

        try:
            # Récupération des rapports annuels
            income = tk.financials
            balance = tk.balance_sheet
            cashflow = tk.cashflow
            history = tk.history(period="5y")

            # On boucle sur les années que tu veux (2021 à 2024)
            for year in range(2021, 2025):
                # On cherche la colonne qui correspond à l'année (format datetime dans yfinance)
                col = [c for c in income.columns if str(year) in str(c)]
                if col:
                    date = col[0]
                    # Extraction des données brutes
                    net_inc = income.loc['Net Income', date] if 'Net Income' in income.index else 0
                    fcf = (cashflow.loc['Operating Cash Flow', date] + cashflow.loc['Capital Expenditure', date]) if 'Operating Cash Flow' in cashflow.index else 0
                    op_inc = income.loc['Operating Income', date] if 'Operating Income' in income.index else 0
                    revenue = income.loc['Total Revenue', date] if 'Total Revenue' in income.index else 1 # éviter div par 0
                    equity = balance.loc['Stockholders Equity', date] if 'Stockholders Equity' in balance.index else 1
                    
                    # Remplissage du dictionnaire
                    company_dict[f'Net_Income_{year}'] = net_inc
                    company_dict[f'FCF_{year}'] = fcf
                    company_dict[f'Op_Margin_{year}'] = round(op_inc / revenue, 4)
                    company_dict[f'ROE_{year}'] = round(net_inc / equity, 4)
                    # EPS (Earnings Per Share)
                    company_dict[f'EPS_{year}'] = tk.info.get('trailingEps', 0) if year == 2024 else None
                
            # Note: La Perf_2025 ou les prévisions 2025 demandent souvent un accès API payant 
            # ou sont dans tk.analyst_price_target
            company_dict['Perf_2025'] = tk.info.get('targetMedianPrice', 0)

        except Exception as e:
            print(f"Erreur pour {name}: {e}")

        final_data.append(company_dict)
        time.sleep(1) # Pause pour éviter d'être banni par Yahoo

    # 3. Création du DataFrame final et sauvegarde
    df_v0 = pd.DataFrame(final_data)
    df_v0.to_csv(output_file, index=False)
    print(f"Base de données {output_file} créée avec succès !")

# Lancement
build_v0_database('BDD E PEA.csv', 'BDD V0.csv')