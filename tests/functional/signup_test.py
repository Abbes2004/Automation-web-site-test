import pytest
import time
from selenium.webdriver.common.by import By
from pages.signup_page import SignupPage
from pages.login_page import LoginPage
from utils.data_generator import DataGenerator
from config.config import Config

def test_signup_success(driver):
    """
    TC01: Sign-up - Création d'un nouveau compte client.
    Vérifie qu'un utilisateur peut s'inscrire avec succès et être redirigé vers My Bookings.
    """
    # 1. Initialisation des pages
    login_page = LoginPage(driver)
    signup_page = SignupPage(driver)
    
    # 2. Accès au site
    driver.get(Config.LOGIN_URL)
    
    # Navigation vers le formulaire d'inscription
    login_page.go_to_signup()

    # 3. Préparation des données dynamiques
    first_name = DataGenerator.GUEST_DATA["first_name"]
    last_name = DataGenerator.GUEST_DATA["last_name"]
    unique_email = DataGenerator.generate_random_email()
    password = DataGenerator.PASSWORD_UNIQUE

    # 4. Exécution de l'inscription
    signup_page.complete_signup(
        first_name, 
        last_name, 
        unique_email, 
        password
    )

    # 5. Vérification (Assertions)
    # On laisse un peu de temps pour la redirection vers /my-bookings
    time.sleep(5) 
    
    current_url = driver.current_url
    print(f"\nDEBUG: URL après inscription : {current_url}")

    # --- CORRECTION DE L'ASSERTION ---
    # Au lieu de chercher l'ID 'app', on vérifie si on est sur la bonne page finale
    assert "my-bookings" in current_url, f"ERREUR : L'utilisateur n'a pas été redirigé vers My Bookings. URL actuelle: {current_url}"
    
    # Vérification secondaire : on ne doit plus être sur signup
    assert "signup" not in current_url, "ERREUR : L'utilisateur est resté bloqué sur la page d'inscription"
    
    print(f"SUCCÈS : TC01 réussi ! Compte créé pour {first_name} ({unique_email})")