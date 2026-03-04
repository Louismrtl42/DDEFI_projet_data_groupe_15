import pandas as pd

def add_sector_and_save_V3():
    # 1. Chargement de la source contenant les secteurs
    # engine='python' avec sep=None permet de détecter automatiquement virgule ou point-virgule
    df_source = pd.read_csv('BDD V0.csv', sep=None, engine='python')
    
    # Nettoyage de l'ISIN pour garantir la correspondance
    df_source['ISIN'] = df_source['ISIN'].astype(str).str.strip()
    
    # Identification de la colonne secteur dans la source
    sector_col_name = 'Sector' if 'Sector' in df_source.columns else 'Secteur'
    
    # On ne garde que ISIN et Sector
    df_sectors = df_source[['ISIN', sector_col_name]].drop_duplicates(subset=['ISIN'])

    def process_file(file_name, output_name):
        df = pd.read_csv(file_name)
        df['Isin'] = df['Isin'].astype(str).str.strip()
        
        # Fusion pour ajouter le secteur
        df_ml4 = pd.merge(df, df_sectors, left_on='Isin', right_on='ISIN', how='left')
        
        # Supprimer la colonne ISIN en double
        if 'ISIN' in df_ml4.columns:
            df_ml4 = df_ml4.drop(columns=['ISIN'])

        # --- RÉORGANISATION DES COLONNES ---
        # On récupère toutes les colonnes
        cols = list(df_ml4.columns)
        # On déplace le secteur (qui est en dernier) en index 1 (deuxième colonne)
        # On retire le nom de la colonne secteur de la liste et on l'insère après 'Name'
        cols.insert(1, cols.pop(cols.index(sector_col_name)))
        
        df_ml4 = df_ml4[cols]
        
        # Sauvegarde
        df_ml4.to_csv(output_name, index=False)
        print(f"✅ Fichier créé : {output_name}")
        print(f"   Structure : {df_ml4.columns[0]}, {df_ml4.columns[1]}, {df_ml4.columns[2]}...")

    # Application
    process_file('BDD_Etalonnage_80.csv', 'BDD_Etalonnage_80_V3.csv')
    process_file('BDD_Test_20.csv', 'BDD_Test_20_V3.csv')

if __name__ == "__main__":
    add_sector_and_save_V3()