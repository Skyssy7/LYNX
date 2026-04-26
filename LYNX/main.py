#!/usr/bin/env python3
import sys
import logging
from src.ui import setup_logging, UI
from src.crypto import CryptoManager
from src.config import Config

def main():
    setup_logging()
    
    manager = CryptoManager()
    
    while True:
        UI.header()
        print("   1. Générer une nouvelle clé maître")
        print("   2. Crypter un fichier")
        print("   3. Décrypter un fichier")
        print("   4. Quitter")
        print("─" * 75)

        choice = input("\n   Votre choix : ").strip()

        if choice == "1":
            manager.key_manager.generate_key()
        elif choice == "2":
            manager.encrypt_file()
        elif choice == "3":
            manager.decrypt_file()
        elif choice == "4":
            UI.header("Lynx")
            print("\n   Au revoir 👋")
            print("   Merci d'avoir utilisé Lynx v" + Config.VERSION)
            logging.info("Lynx arrêté par l'utilisateur")
            import time
            time.sleep(2)
            break
        else:
            UI.error("Choix invalide.")

        if choice != "4":
            UI.wait()

    logging.info("=== Lynx v" + Config.VERSION + " arrêté ===")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n   Arrêt du programme.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Erreur critique inattendue: {e}", exc_info=True)
        print(f"\n   Erreur inattendue : {e}")