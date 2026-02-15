import pandas as pd
from sqlalchemy import create_engine, text
import os

def load_data_to_sql():
    print("💾 Démarrage du chargement en base SQL...")
    
    # 1. Lire le CSV nettoyé
    input_path = "data/clean_stock_data.csv"
    if not os.path.exists(input_path):
        print("❌ Erreur : clean_stock_data.csv introuvable.")
        return

    df = pd.read_csv(input_path)
    print(f"   Lecture de {len(df)} lignes depuis le CSV.")
    
    # 2. Créer la connexion à la base de données (SQLite)
    # Dans une vraie boite, on mettrait ici : 'postgresql://user:password@localhost/db'
    engine = create_engine('sqlite:///trading.db')
    
    # 3. Charger les données dans la table 'market_data'
    # if_exists='replace' : Si la table existe déjà, on l'écrase (utile pour tester)
    # index=False : On ne veut pas sauvegarder l'index pandas (0, 1, 2...)
    try:
        df.to_sql('market_data', con=engine, if_exists='replace', index=False)
        print("✅ Données insérées avec succès dans la table 'market_data' !")
        
        # 4. Petite vérification (On fait une requête SQL SELECT)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM market_data LIMIT 3"))
            print("\n🔍 Vérification (3 premières lignes de la BDD) :")
            for row in result:
                print(row)
                
    except Exception as e:
        print(f"❌ Erreur SQL : {e}")

if __name__ == "__main__":
    load_data_to_sql()