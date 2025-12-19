import os

class Config:
    # --- URLs de base ---
    BASE_URL = "https://dbarberzzdemo.trafft.com"
    LOGIN_URL = f"{BASE_URL}/login"
    SIGNUP_URL = f"{BASE_URL}/signup" # URL déduite pour l'inscription
    MY_BOOKINGS_URL = f"{BASE_URL}/my-bookings"

    # --- Paramètres du Driver ---
    # Changez "chrome" par "firefox" ou "edge" pour le cross-browser global
    DEFAULT_BROWSER = "chrome"
    # Mettre à True pour exécuter les tests sans ouvrir la fenêtre du navigateur
    HEADLESS_MODE = False
    
    # --- Délais (Timeouts) ---
    # Temps d'attente maximum pour les éléments (WaitUtils)
    EXPLICIT_WAIT = 15 
    # Temps d'attente implicite de sécurité
    IMPLICIT_WAIT = 5

    # --- Chemins des fichiers (Logs et Rapports) ---
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # Pourrait servir pour stocker les captures d'écran des bugs trouvés
    SCREENSHOT_DIR = os.path.join(ROOT_DIR, "..", "reports", "screenshots")