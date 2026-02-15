import pandas as pd
import numpy as np

def calculate_rsi(data, window=14):
    """
    Calcule le RSI (Relative Strength Index) manuellement.
    C'est un excellent exercice d'algo pour un entretien.
    """
    delta = data['Close'].diff()
    
    # On sépare les gains (positifs) et les pertes (négatives)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def transform_data():
    print("⚙️ Début de la transformation...")
    
    # 1. Charger les données brutes
    input_path = "data/raw_stock_data.csv"
    if not os.path.exists(input_path):
        print("❌ Erreur : Le fichier raw_stock_data.csv n'existe pas. Lance extract.py d'abord.")
        return

    df = pd.read_csv(input_path)
    
    # IMPORTANT : Convertir la date en format datetime (sinon Pandas ne comprend pas l'ordre)
    df['Date'] = pd.to_datetime(df['Date'],utc=True)
    df.sort_values(by=['Symbol', 'Date'], inplace=True)
    
    # 2. Calcul des indicateurs PAR GROUPE (par action)
    # On ne veut pas que la moyenne mobile de TotalEnergies mélange les prix d'AXA !
    
    df['SMA_20'] = df.groupby('Symbol')['Close'].transform(lambda x: x.rolling(window=20).mean())
    
    # Calcul du RSI (plus complexe, on l'applique par groupe aussi)
    df['RSI'] = df.groupby('Symbol').apply(lambda x: calculate_rsi(x)).reset_index(level=0, drop=True)
    
    # 3. Nettoyage final
    # Les 20 premières lignes auront des NaN (car pas assez d'historique pour la moyenne), on les vire.
    df.dropna(inplace=True)
    
    # 4. Sauvegarde
    output_path = "data/clean_stock_data.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✅ Transformation terminée ! Données propres sauvegardées dans : {output_path}")
    print(df.tail()) # Affiche les dernières lignes pour vérifier

import os
if __name__ == "__main__":
    transform_data()