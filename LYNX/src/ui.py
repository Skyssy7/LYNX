import os
import logging
import sys
from pathlib import Path
from tqdm import tqdm
from .config import Config

class UI:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def header(title: str = "LYNX"):
        UI.clear()
        os.system(f'title {title}')
        print("\n" + "═" * 75)
        print(f"🔐 {title}".center(75))
        print("═" * 75)

    @staticmethod
    def success(msg: str):
        print(f"   ✅ {msg}")

    @staticmethod
    def error(msg: str):
        print(f"   ❌ {msg}")

    @staticmethod
    def info(msg: str):
        print(f"   ℹ️  {msg}")

    @staticmethod
    def progress(description: str, total: int):
        return tqdm(
            total=total,
            desc=f"   {description}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            leave=True,
            file=sys.stdout
        )

    @staticmethod
    def wait():
        input("\n   Appuyez sur Entrée pour continuer...")

def setup_logging():
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        filename="logs/lynx.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.info(f"=== Lynx v{Config.VERSION} démarré ===")