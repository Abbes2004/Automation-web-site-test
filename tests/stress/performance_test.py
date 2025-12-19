import pytest
import time
from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.booking_page import BookingPage
from config.config import Config
from utils.data_generator import DataGenerator

def test_tc22_location_loading_time():
    driver = DriverFactory.get_driver("chrome")
    driver.maximize_window()
    
    login_page = LoginPage(driver)
    booking_page = BookingPage(driver)
    
    try:
        # 1. Préparation : Arriver jusqu'à l'étape juste avant les locations
        driver.get(Config.LOGIN_URL)
        login_page.login("zz@gmail.com", DataGenerator.PASSWORD_UNIQUE)
        
        booking_page.click_book_now_nav()
        booking_page.expand_services_list()
        booking_page.select_first_service()
        booking_page.click_continue() # Étape Extras
        
        # Sélection du Barber pour arriver à l'écran des Locations
        print("[ACTION] Sélection du Barber pour déclencher le chargement des locations...")
        
        # --- MESURE DE PERFORMANCE ---
        start_time = time.time() # Timestamp de début
        
        booking_page.choose_first_available() # Clic qui charge les locations
        
        # On attend que le bouton de choix de location apparaisse (preuve de chargement)
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(booking_page.CHOOSE_OPTION_BTN)
        )
        
        end_time = time.time() # Timestamp de fin
        # -----------------------------

        loading_duration = end_time - start_time
        print(f"\n[METRIC] Temps de chargement des locations : {loading_duration:.2f} secondes")

        # ASSERTION : Moins de 2 secondes
        assert loading_duration <= 2.0, f"ALERTE PERF : Chargement trop lent ({loading_duration:.2f}s)"
        print("[SUCCESS] Le temps de chargement est conforme aux exigences (<= 2s).")

    finally:
        driver.quit()