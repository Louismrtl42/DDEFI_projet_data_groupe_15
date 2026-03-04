import pandas as pd

def split_database(input_file, train_ratio=0.8):
    # 1. Chargement de la base propre
    df = pd.read_csv(input_file)
    
    # 2. Mélange aléatoire des données pour éviter les biais 
    # (ex: si le fichier est trié par secteur ou par ordre alphabétique)
    df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # 3. Calcul de l'indice de séparation
    split_index = int(len(df_shuffled) * train_ratio)
    
    # 4. Création des deux sets
    df_train = df_shuffled.iloc[:split_index]
    df_test = df_shuffled.iloc[split_index:]
    
    # 5. Sauvegarde
    df_train.to_csv('BDD_Etalonnage_80.csv', index=False)
    df_test.to_csv('BDD_Test_20.csv', index=False)
    
    print(f"Division terminée :")
    print(f"- Base Etalonnage (80%) : {len(df_train)} entreprises")
    print(f"- Base Test (20%) : {len(df_test)} entreprises")

# Lancement du split
split_database('BDD_Finale.csv')