from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import logging
from getpass import getpass
from .config import Config
from .key_manager import KeyManager
from .ui import UI

class CryptoManager:
    def __init__(self):
        self.key_manager = KeyManager()

    def _derive_key(self, password: str) -> bytes | None:
        if not self.key_manager.salt_file.exists():
            UI.error("Aucune clé trouvée. Créez-en une avec l'option 1.")
            return None

        if not self.key_manager.verify_password(password):
            UI.error("Mot de passe incorrect.")
            return None

        try:
            with open(self.key_manager.salt_file, "rb") as f:
                salt = f.read()

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=Config.PBKDF2_ITERATIONS,
            )
            return base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        except Exception as e:
            logging.error(f"Erreur dérivation clé : {e}")
            UI.error("Erreur interne lors de la dérivation de la clé.")
            return None

    def encrypt_file(self):
        UI.header("Cryptage")
        password = getpass("   Mot de passe maître : ")
        
        key = self._derive_key(password)
        if not key:
            return

        path = input("\n   Chemin du fichier à crypter : ").strip().strip('"')
        file_path = Path(path)

        if not file_path.exists():
            UI.error("Fichier introuvable.")
            return

        try:
            data = file_path.read_bytes()
            
            if len(data) > Config.PROGRESS_THRESHOLD:
                with UI.progress("Cryptage en cours", len(data)) as pbar:
                    fernet = Fernet(key)
                    encrypted = fernet.encrypt(data)
                    pbar.update(len(data))
            else:
                fernet = Fernet(key)
                encrypted = fernet.encrypt(data)

            output_file = file_path.with_suffix(file_path.suffix + ".cry")
            output_file.write_bytes(encrypted)
            file_path.unlink()

            UI.success(f"Fichier crypté : {output_file.name}")
            logging.info(f"CRYPTAGE | {file_path.name} → {output_file.name}")
        except Exception as e:
            logging.error(f"Erreur cryptage {file_path.name}: {e}")
            UI.error("Erreur lors du cryptage.")

    def decrypt_file(self):
        UI.header("Décryptage")
        password = getpass("   Mot de passe maître : ")
        
        key = self._derive_key(password)
        if not key:
            return

        path = input("\n   Chemin du fichier à décrypter : ").strip().strip('"')
        file_path = Path(path)

        if not file_path.exists():
            UI.error("Fichier introuvable.")
            return

        try:
            data = file_path.read_bytes()
            
            if len(data) > Config.PROGRESS_THRESHOLD:
                with UI.progress("Décryptage en cours", len(data)) as pbar:
                    fernet = Fernet(key)
                    decrypted = fernet.decrypt(data)
                    pbar.update(len(data))
            else:
                fernet = Fernet(key)
                decrypted = fernet.decrypt(data)

            original_name = file_path.name[:-4] if file_path.name.lower().endswith(".cry") else file_path.name
            output_file = file_path.with_name(original_name)

            output_file.write_bytes(decrypted)
            file_path.unlink()

            UI.success(f"Fichier décrypté : {output_file.name}")
            logging.info(f"DÉCRYPTAGE | {output_file.name}")
        except InvalidToken:
            UI.error("Mot de passe incorrect.")
        except Exception as e:
            logging.error(f"Erreur décryptage {file_path.name}: {e}")
            UI.error("Erreur lors du décryptage.")