# 🔐 Lynx - Chiffrement de Fichiers

**Lynx** est un outil de chiffrement de fichiers **simple, rapide et sécurisé**, conçu pour protéger vos documents, photos, vidéos et données sensibles sur votre ordinateur.

---

## ✨ Fonctionnalités

- Chiffrement/déchiffrement ultra-rapide avec **AES-256 (Fernet)**
- Protection du mot de passe maître avec **Argon2id** (256 Mo de mémoire)
- Dérivation de clé renforcée (**PBKDF2** à 650 000 itérations)
- Barre de progression intelligente pour les gros fichiers
- Interface console propre et intuitive
- Journalisation complète des opérations
- Suppression automatique du fichier original après chiffrement

---

## 🛡️ Sécurité

- **Algorithme** : AES-256 + HMAC
- **Hash du mot de passe** : Argon2id (résistant aux attaques GPU/ASIC)
- **Mémoire Argon2** : 256 Mo
- **Aucune donnée** n’est envoyée sur internet

---

## 🚀 Installation & Utilisation

```bash
# 1. Clonez ou téléchargez le projet
git clone https://github.com/votre-nom/lynx.git
cd lynx

# 2. Installez les dépendances
pip install -r requirements.txt

# 3. Lancez Lynx
python main.py