import os
import logging
from pathlib import Path
from typing import Optional

class UI:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def header(title: str = "LYNX"):
        UI.clear()
        os.system(f'title {title}')
        print("\n" + "═" * 70)
        print(f"🔐 {title}".center(70))
        print("═" * 70)
    
    @staticmethod
    def success(msg: str):
        print(f"   ✅ {msg}")
    
    @staticmethod
    def error(msg: str):
        print(f"   ❌ {msg}")
    
    @staticmethod
    def info(msg: str):
        print(f"   ℹ️  {msg}")

def setup_logging():
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        filename="logs/lynx.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.info("=== Lynx v2.1 démarré ===")