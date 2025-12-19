import pytest
import time
from pages.login_page import LoginPage
from config.config import Config

def test_login_invalid_password(driver):
    """
    TC03: Sign-in Négatif - Connexion avec un mot de passe erroné.
    Vérifie que l'accès est refusé et qu'un message d'erreur s'affiche.
    """
    # 1. Initialisation
    login_page = LoginPage(driver)
    
    # 2. Accès à la page
    driver.get(Config.LOGIN_URL)
    
    # 3. Saisie des identifiants (Email correct, mais mot de passe faux)
    test_email = "abbesamine01@gmail.com"
    wrong_password = "MauvaisMotDePasse123"

    print(f"\n[INFO] Test de sécurité : tentative avec un mot de passe erroné.")
    
    login_page.enter_email(test_email)
    login_page.enter_password(wrong_password)
    
    # 4. Clic sur Log In
    login_page.click_login_submit()

    # 5. Vérification (Assertion)
    # On attend un peu que le message d'erreur apparaisse
    time.sleep(4) 
    
    error_message = login_page.get_error_message()
    current_url = driver.current_url

    print(f"\n[DEBUG] Message d'erreur capturé : {error_message}")
    print(f"[DEBUG] URL actuelle : {current_url}")

    # --- ASSERTIONS ---
    
    # A. Vérification que le message n'est pas None
    assert error_message is not None, "ÉCHEC : L'alerte 'ui-alert' n'a pas été détectée dans le DOM."
    
    # B. Vérification du contenu du message (basé sur ton HTML)
    # Ton HTML contient : "Invalid username or password. Please try again."
    expected_keyword = "Invalid"
    assert expected_keyword in error_message, f"ÉCHEC : Le message attendu '{expected_keyword}' est absent de : '{error_message}'"
    
    # C. Sécurité : L'URL ne doit pas être celle du dashboard
    assert "my-bookings" not in current_url, "ÉCHEC CRITIQUE : Redirection vers My Bookings malgré un mot de passe erroné !"

    print(f"RÉSULTAT : TC03 réussi. L'erreur a été correctement détectée et validée.")