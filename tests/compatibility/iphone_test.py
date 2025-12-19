import pytest
import time
from tests.conftest import driver
from utils.data_generator import DataGenerator
from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.my_bookings_page import MyBookingsPage
from config.config import Config

def test_responsive_mobile_iphone():
    # Initialisation Chrome
    driver = DriverFactory.get_driver("chrome")
    
    try:
        # Résolution iPhone 12/13
        driver.set_window_size(390, 844)
        print("\n[INFO] Test Mobile : Résolution 390x844 (iPhone 12/13)")

        login_page = LoginPage(driver)
        my_bookings_page = MyBookingsPage(driver)

        # 1. Connexion
        driver.get(Config.LOGIN_URL)
        login_page.login("zz@gmail.com", DataGenerator.PASSWORD_UNIQUE)
        time.sleep(3)

        # 2. Action sur le bouton de la page My Bookings
        print("[ACTION] Clic sur le bouton 'Book Now' de la page My Bookings")
        my_bookings_page.click_book_now_main()
        time.sleep(3)

        # 3. Validation du succès : Redirection vers le choix de service
        # 3. Validation du succès : Redirection vers la page de réservation
        current_url = driver.current_url
        # On vérifie si 'booking' ou 'service' est dans l'URL
        assert "booking" in current_url.lower() or "service" in current_url.lower(), f"ÉCHEC : Redirection incorrecte ({current_url})"
        print(f"[SUCCESS] TC19 : Redirection réussie sur iPhone. URL actuelle : {current_url}")

    finally:
        driver.quit()