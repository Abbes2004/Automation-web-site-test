import pytest
import time
from pages.booking_page import BookingPage
from config.config import Config

def test_invalid_phone_format_letters(driver):
    """
    TC09: Limites (BVA/Format) - Numéro de téléphone avec des lettres.
    Vérifie que le formulaire bloque la validation et affiche l'erreur.
    """
    booking_page = BookingPage(driver)
    invalid_phone = "66562"

    # 1. Navigation jusqu'au formulaire Guest
    driver.get(Config.BASE_URL)
    booking_page.click_book_now_nav()
    time.sleep(2)
    booking_page.expand_services_list()
    booking_page.select_first_service()
    time.sleep(1)
    booking_page.click_continue() # Extras
    booking_page.choose_first_available() # Barber
    booking_page.choose_first_available() # Location
    booking_page.select_first_time()
    booking_page.click_continue()
    time.sleep(1)
    booking_page.click_continue() # Recurring
    time.sleep(2)

    # 2. Saisie des informations avec un téléphone invalide
    booking_page.fill_guest_info("Amine", "Abbes", "phone.test@gmail.com", "none")
    booking_page.fill_phone(invalid_phone)
    
    # 3. Tentative de validation pour déclencher l'erreur
    booking_page.click_continue_or_book()
    time.sleep(2)

    # 4. Vérification du message d'erreur
    error_text = booking_page.get_phone_error()
    expected_error = "Please enter a valid phone number"

    print(f"[DEBUG] Erreur détectée : {error_text}")

    assert error_text == expected_error, f"ERREUR : Le message attendu était '{expected_error}', mais a reçu '{error_text}'"
    
    print("[SUCCESS] Le formulaire a correctement bloqué le format téléphone invalide.")