import pytest
import time
from pages.login_page import LoginPage
from config.config import Config
from utils.data_generator import DataGenerator

def test_login_email_uppercase(driver):
    """
    TC04: Sign-in Casse - Connexion avec l'email en MAJUSCULES.
    Vérifie que le système normalise l'email et autorise l'accès.
    """
    # 1. Initialisation
    login_page = LoginPage(driver)
    
    # 2. Accès à la page
    driver.get(Config.LOGIN_URL)
    
    # 3. Préparation des identifiants (Email en MAJUSCULES)
    original_email = "abbesamine01@gmail.com"
    uppercase_email = original_email.upper() # "ABBESAMINE01@GMAIL.COM"
    password = DataGenerator.PASSWORD_UNIQUE 

    print(f"\n[INFO] Test de normalisation : tentative avec l'email en MAJUSCULES.")
    print(f"[DEBUG] Email saisi : {uppercase_email}")
    
    # 4. Saisie et clic
    login_page.enter_email(uppercase_email)
    login_page.enter_password(password)
    login_page.click_login_submit()

    # 5. Vérification (Assertion)
    # On laisse le temps à la redirection
    time.sleep(5)
    
    current_url = driver.current_url
    print(f"[DEBUG] URL après soumission : {current_url}")

    # --- ASSERTIONS ---
    # L'accès doit être autorisé malgré les majuscules
    assert "my-bookings" in current_url, (
        f"ÉCHEC : Le système est sensible à la casse. "
        f"L'URL actuelle est {current_url} au lieu de my-bookings."
    )
    
    # Vérification qu'aucun message d'erreur n'est apparu
    error_message = login_page.get_error_message()
    assert error_message is None, f"ÉCHEC : Une erreur est apparue : {error_message}"

    print(f"RÉSULTAT : TC04 réussi. L'email a été correctement normalisé par le serveur.")