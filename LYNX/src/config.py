from pathlib import Path

class Config:
    APP_NAME = "LYNX"
    VERSION = "3.0.0"
    
    SALT_FILE = Path("salt.bin")
    HASH_FILE = Path("master.hash")
    CONFIG_FILE = Path("config.toml")
    
    # Sécurité
    PBKDF2_ITERATIONS = 650000
    ARGON2_TIME_COST = 4
    ARGON2_MEMORY_COST = 262144
    ARGON2_PARALLELISM = 4
    
    MIN_PASSWORD_LENGTH = 8
    
    # Performance
    PROGRESS_THRESHOLD = 50 * 1024 * 1024  # 50 Mo → à partir de là on affiche une barre de progression