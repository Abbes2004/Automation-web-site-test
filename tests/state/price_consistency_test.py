import pytest
import time
import re
from pages.login_page import LoginPage
from pages.booking_page import BookingPage
from pages.my_bookings_page import MyBookingsPage
from config.config import Config
from utils.data_generator import DataGenerator
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_price_consistency_final_verification(driver):
    login_page = LoginPage(driver)
    booking_page = BookingPage(driver)
    my_bk_page = MyBookingsPage(driver)
    wait = WebDriverWait(driver, 15)

    # --- ÉTAPE 1 : PARCOURS DE BOOKING COMPLET (Mémorisé) ---
    print("\n[STEP 1] Exécution du tunnel de réservation complet...")
    driver.get(Config.LOGIN_URL)
    login_page.login("abbesamine01@gmail.com", DataGenerator.PASSWORD_UNIQUE)
    
    booking_page.click_book_now_nav()
    booking_page.expand_services_list()
    booking_page.select_first_service()
    booking_page.click_continue()         # Étape Extras
    booking_page.choose_first_available() # Étape Barber
    booking_page.choose_first_available() # Étape Location
    booking_page.select_first_time()      # Étape Time
    booking_page.click_continue()
    booking_page.click_continue()         # Étape Recurring
    booking_page.fill_allergies("yes")
    booking_page.click_continue_or_book() # Validation vers paiement/confirmation
    
    if not booking_page.is_booking_confirmed():
        booking_page.confirm_final_booking()

    # --- ÉTAPE 2 : EXTRACTION DU PRIX SUR L'ÉCRAN DE SUCCÈS (Ton image) ---
    print("[STEP 2] Extraction du prix depuis le panneau 'Booking Details'...")
    
    # On attend que le message de succès soit bien là
    wait.until(EC.visibility_of_element_located(booking_page.SUCCESS_CONFIRMATION))
    
    # Extraction JS du prix dans le panneau de droite (h5 text-primary)
    js_extract_final_price = """
        let priceElement = document.querySelector('.booking-details-body__item__content h5.text-primary');
        return priceElement ? priceElement.innerText : null;
    """
    raw_price_success = driver.execute_script(js_extract_final_price)
    
    if not raw_price_success:
        pytest.fail("Impossible d'extraire le prix du panneau récapitulatif.")

    # Nettoyage : Si "$55 / $55", on ne garde que le premier "55"
    price_confirmed = re.search(r"(\d+)", raw_price_success).group(1)
    print(f"[INFO] Prix extrait de la confirmation : {price_confirmed}$")

    # --- ÉTAPE 3 : VÉRIFICATION DANS 'MY BOOKINGS' ---
    print("[STEP 3] Navigation vers 'My Bookings' pour vérification...")
    driver.get(f"{Config.BASE_URL}/my-bookings")
    
    # Ouverture du dernier booking (le panel s'ouvre au clic)
    last_item = wait.until(EC.element_to_be_clickable(my_bk_page.LAST_BOOKING_ITEM))
    driver.execute_script("arguments[0].click();", last_item)
    
    # Extraction du prix dans le panel de détails ouvert
    js_extract_history_price = """
        let h5 = document.querySelector('.flex.flex-col.gap-1 h5');
        return h5 ? h5.innerText : null;
    """
    raw_price_history = driver.execute_script(js_extract_history_price)
    price_history = re.search(r"(\d+)", raw_price_history).group(1)
    print(f"[INFO] Prix extrait de l'historique : {price_history}$")

    # --- ÉTAPE 4 : COMPARAISON ---
    assert price_confirmed == price_history, f"ERREUR : {price_confirmed}$ (Confirmation) != {price_history}$ (Historique)"
    print(f"[SUCCESS] TC15 : Les données sont cohérentes entre le succès et l'historique.")