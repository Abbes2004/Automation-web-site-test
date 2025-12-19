import pytest
import time
from pages.login_page import LoginPage
from config.config import Config
from utils.data_generator import DataGenerator # Import important

def test_login_success(driver):
    """
    TC02: Sign-in - Connexion avec des identifiants valides.
    """
    login_page = LoginPage(driver)
    driver.get(Config.LOGIN_URL)
    
    # --- FIX DES DONNÉES ---
    test_email = "abbesamine01@gmail.com"
    # On utilise la variable centralisée de ton DataGenerator
    test_password = DataGenerator.PASSWORD_UNIQUE 

    print(f"\n[INFO] Tentative avec l'email: {test_email} et le pass: {test_password}")
    
    login_page.enter_email(test_email)
    login_page.enter_password(test_password)
    login_page.click_login_submit()

    # Vérification
    time.sleep(5)
    current_url = driver.current_url
    error_found = login_page.get_error_message()
    
    assert "my-bookings" in current_url, f"ÉCHEC : Mot de passe rejeté par le site. Message : {error_found}"
    
    print(f"RÉSULTAT : TC02 réussi avec le mot de passe {test_password}")