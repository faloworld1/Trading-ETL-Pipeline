import yfinance as yf
import pandas as pd
import os

# Liste des entreprises du CAC 40 qui t'intéressent (Banque, Assurance, Énergie)
TICKERS = ["TTE.PA", "CS.PA", "BNP.PA", "GLE.PA"] 
# TTE=Total, CS=AXA, BNP=BNP Paribas, GLE=Société Générale

def extract_stock_data(tickers, period="5y"):
    """
    Récupère les données historiques pour une liste d'actions.
    """
    print(f"🔄 Démarrage de l'extraction pour : {tickers}")
    
    # Création d'une liste pour stocker les DataFrames
    all_data = []
    
    for ticker in tickers:
        try:
            # Appel à l'API Yahoo Finance
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)
            
            # On ajoute une colonne pour savoir de quelle action il s'agit
            df['Symbol'] = ticker
            
            # On réinitialise l'index pour avoir la Date en colonne normale
            df.reset_index(inplace=True)
            
            # On garde uniquement les colonnes utiles
            df = df[['Date', 'Symbol', 'Close', 'Volume']]
            
            all_data.append(df)
            print(f"✅ {ticker} : {len(df)} lignes récupérées.")
            
        except Exception as e:
            print(f"❌ Erreur pour {ticker} : {e}")

    # On combine tout dans un seul grand tableau
    if all_data:
        final_df = pd.concat(all_data)
        return final_df
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    # 1. Extraction
    df_cac = extract_stock_data(TICKERS)
    
    # 2. Sauvegarde temporaire (Raw Data)
    # Créer le dossier 'data' s'il n'existe pas
    if not os.path.exists("data"):
        os.makedirs("data")
        
    csv_path = "data/raw_stock_data.csv"
    df_cac.to_csv(csv_path, index=False)
    
    print(f"\n🎉 Extraction terminée ! Fichier sauvegardé ici : {csv_path}")
    print(df_cac.head()) # Affiche les 5 premières lignes