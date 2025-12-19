import pytest
import time
from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.my_bookings_page import MyBookingsPage
from config.config import Config
from utils.data_generator import DataGenerator

def test_responsive_tablet_ipad():
    # 1. Initialisation du driver Chrome
    driver = DriverFactory.get_driver("chrome")
    
    try:
        # 2. Configuration de la résolution iPad (768 x 1024)
        driver.set_window_size(768, 1024)
        print("\n[INFO] Test Tablette : Résolution 768x1024 (iPad)")

        login_page = LoginPage(driver)
        my_bookings_page = MyBookingsPage(driver)

        # 3. Connexion
        driver.get(Config.LOGIN_URL)
        # On utilise DataGenerator comme dans votre script iPhone
        login_page.login("zz@gmail.com", DataGenerator.PASSWORD_UNIQUE)
        
        # Attente pour laisser le dashboard se charger sur tablette
        time.sleep(5)

        # 4. Action sur le bouton "Book Now" de la page My Bookings
        print("[ACTION] Clic sur le bouton 'Book Now' de la page My Bookings (Vue Tablette)")
        my_bookings_page.click_book_now_main()
        
        # Attente de la redirection
        time.sleep(3)

        # 5. Validation du succès (Oracle de test mis à jour avec 'booking')
        current_url = driver.current_url
        assert "booking" in current_url.lower() or "service" in current_url.lower(), \
            f"ÉCHEC : Redirection incorrecte sur iPad. URL actuelle : {current_url}"
        
        print(f"[SUCCESS] TC20 : Redirection réussie sur iPad. URL : {current_url}")

    finally:
        # 6. Fermeture propre du navigateur
        driver.quit()