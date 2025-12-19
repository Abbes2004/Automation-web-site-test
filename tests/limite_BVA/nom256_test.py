import pytest
import time
from pages.booking_page import BookingPage
from config.config import Config
from utils.data_generator import DataGenerator

def test_bva_name_limit_256_blocked(driver):
    """
    TC08: Limites (BVA) - Tentative de saisie de 256 caractères.
    Vérifie que l'interface bloque la saisie à 255 (Maxlength).
    """
    booking_page = BookingPage(driver)
    input_name = DataGenerator.TOO_LONG_NAME # 256 caractères

    # 1. Accès direct à la page de réservation (Guest)
    driver.get(Config.BASE_URL)
    booking_page.click_book_now_nav()
    time.sleep(3)
    
    # 2. Navigation rapide jusqu'au formulaire
    booking_page.expand_services_list()
    booking_page.select_first_service()
    time.sleep(1)
    booking_page.click_continue()
    time.sleep(1)
    booking_page.choose_first_available() # Barber
    time.sleep(1)
    booking_page.choose_first_available() # Location
    time.sleep(1)
    booking_page.select_first_time()
    booking_page.click_continue()
    time.sleep(2)
    booking_page.click_continue() # Recurring
    time.sleep(2)

    # 3. Section Critique : Tentative de saisie de 256 caractères
    print(f"[ACTION] Test BVA Négatif : Tentative de saisie de {len(input_name)} caractères.")
    
    # On saisit le nom trop long
    booking_page.fill_guest_info(
        first=input_name, 
        last="Test", 
        email="bva.invalid@test.com", 
        allergies="none"
    )

    # 4. Vérification du blocage (Assertion)
    # On récupère ce qui a réellement été écrit dans le champ
    time.sleep(2)
    element = driver.find_element(*booking_page.GUEST_FIRST_NAME)
    actual_value = element.get_attribute("value")
    actual_length = len(actual_value)
    time.sleep(2)

    print(f"[DEBUG] Taille attendue : 255 | Taille réelle après blocage : {actual_length}")

    # Le test réussit si la taille réelle est de 255 (donc le 256ème a été bloqué)
    assert actual_length == 255, f"ERREUR : Le champ a accepté {actual_length} caractères au lieu de bloquer à 255."
    assert actual_length != len(input_name), "ERREUR : Le 256ème caractère a été accepté !"

    print("[SUCCESS] L'interface a correctement bloqué la saisie à 255 caractères.")