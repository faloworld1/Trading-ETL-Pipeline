import extract
import transform
import load
import time

def run_pipeline():
    start_time = time.time()
    print("🚀 DÉMARRAGE DU PIPELINE DE TRADING 🚀")
    print("-" * 40)
    
    # Étape 1 : Extraction
    try:
        print("\n📥 [ETAPE 1/3] EXTRACTION...")
        # On définit nos tickers ici (plus propre que dans extract.py)
        TICKERS = ["TTE.PA", "CS.PA", "BNP.PA", "GLE.PA", "MC.PA"] # Ajout LVMH
        
        df = extract.extract_stock_data(TICKERS)
        
        # Sauvegarde temporaire
        import os
        if not os.path.exists("data"):
            os.makedirs("data")
        df.to_csv("data/raw_stock_data.csv", index=False)
        print("✅ Extraction terminée avec succès.")
        
    except Exception as e:
        print(f"❌ CRASH lors de l'extraction : {e}")
        return # On arrête tout si l'extraction plante

    # Étape 2 : Transformation
    try:
        print("\n⚙️ [ETAPE 2/3] TRANSFORMATION...")
        transform.transform_data()
        # Note : transform_data() lit raw_stock_data.csv et écrit clean_stock_data.csv
        print("✅ Transformation terminée avec succès.")
    except Exception as e:
        print(f"❌ CRASH lors de la transformation : {e}")
        return

    # Étape 3 : Chargement
    try:
        print("\n💾 [ETAPE 3/3] CHARGEMENT SQL...")
        load.load_data_to_sql()
        print("✅ Chargement terminé avec succès.")
    except Exception as e:
        print(f"❌ CRASH lors du chargement : {e}")
        return

    end_time = time.time()
    duration = round(end_time - start_time, 2)
    print("-" * 40)
    print(f"🎉 PIPELINE TERMINÉ EN {duration} SECONDES ! 🎉")
    print("Tes données sont prêtes dans 'trading.db'.")

if __name__ == "__main__":
    run_pipeline()