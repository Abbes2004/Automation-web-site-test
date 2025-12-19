import pytest
import time
from pages.booking_page import BookingPage
from config.config import Config
from utils.data_generator import DataGenerator

def test_bva_name_limit_255(driver):
    """
    TC07: Limites (BVA) - Saisie de 255 caractères dans Nom/Prénom.
    Vérifie que le système accepte la limite maximale autorisée.
    """
    booking_page = BookingPage(driver)
    long_name = DataGenerator.LONG_NAME

    # 1. Accès et navigation jusqu'au formulaire (Réutilisation du flux Guest)
    driver.get(Config.BASE_URL)
    booking_page.click_book_now_nav()
    time.sleep(3)
    
    booking_page.expand_services_list()
    booking_page.select_first_service()
    time.sleep(2)
    booking_page.click_continue() # Extras
    time.sleep(2)
    booking_page.choose_first_available() # Barber
    time.sleep(2)
    booking_page.choose_first_available() # Location
    time.sleep(2)
    booking_page.select_first_time() # Date/Time
    booking_page.click_continue()
    time.sleep(2)
    booking_page.click_continue() # Recurring
    time.sleep(2)

    # 2. Section Critique : Test de la limite BVA
    print(f"[ACTION] Test BVA : Saisie de {len(long_name)} caractères dans First Name.")
    booking_page.fill_guest_info(
        first=long_name, 
        last="Test", 
        email="limit.test@gmail.com", 
        allergies="none"
    )
    
    # 3. Vérification de la valeur saisie (avant de continuer)
    # On récupère la valeur réellement présente dans le champ
    element = driver.find_element(*booking_page.GUEST_FIRST_NAME)
    actual_value = element.get_attribute("value")
    
    assert len(actual_value) == 255, f"ERREUR : La saisie a été tronquée à {len(actual_value)}"
    print("[SUCCESS] Le champ a accepté les 255 caractères.")

    # 4. Finalisation pour vérifier que le système enregistre bien
    booking_page.click_continue_or_book()
    time.sleep(5)
    
    # Note : Si le bouton Book Now est cliquable, le test est réussi
    if not booking_page.is_booking_confirmed():
        booking_page.confirm_final_booking()
        time.sleep(5)

    assert booking_page.is_booking_confirmed(), "ERREUR : Impossible de finaliser avec 255 caractères."