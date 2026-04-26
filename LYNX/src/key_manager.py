from pathlib import Path
from argon2 import PasswordHasher, exceptions as argon_exceptions
from .config import Config
from .ui import UI
import os
import logging
from getpass import getpass

class KeyManager:
    def __init__(self):
        self.ph = PasswordHasher(
            time_cost=Config.ARGON2_TIME_COST,
            memory_cost=Config.ARGON2_MEMORY_COST,
            parallelism=Config.ARGON2_PARALLELISM
        )
        self.salt_file = Config.SALT_FILE
        self.hash_file = Config.HASH_FILE

    def generate_key(self) -> bool:
        UI.header("Création de la clé maître")
        
        pwd1 = getpass("   Créez votre mot de passe maître : ")
        pwd2 = getpass("   Confirmez le mot de passe     : ")

        if pwd1 != pwd2:
            UI.error("Les mots de passe ne correspondent pas.")
            UI.wait()
            return False

        if len(pwd1) < Config.MIN_PASSWORD_LENGTH:
            UI.error(f"Le mot de passe doit faire au moins {Config.MIN_PASSWORD_LENGTH} caractères.")
            UI.wait()
            return False

        try:
            salt = os.urandom(16)
            with open(self.salt_file, "wb") as f:
                f.write(salt)

            argon_hash = self.ph.hash(pwd1)
            with open(self.hash_file, "w", encoding="utf-8") as f:
                f.write(argon_hash)

            logging.info("Clé maître générée avec succès")
            UI.success("Clé maître générée avec succès !")
            UI.wait()
            return True
        except Exception as e:
            logging.error(f"Erreur génération clé: {e}")
            UI.error("Erreur lors de la génération de la clé.")
            UI.wait()
            return False

    def verify_password(self, password: str) -> bool:
        if not self.hash_file.exists():
            UI.error("Aucune clé trouvée. Créez-en une avec l'option 1.")
            return False

        try:
            with open(self.hash_file, "r", encoding="utf-8") as f:
                stored_hash = f.read().strip()
            self.ph.verify(stored_hash, password)
            return True
        except argon_exceptions.VerifyMismatchError:
            return False
        except Exception as e:
            logging.error(f"Erreur vérification mot de passe: {e}")
            return False