import pytest
import time
from pages.booking_page import BookingPage
from config.config import Config

def test_invalid_email_format_no_dot(driver):
    """
    TC11: Limites (Format) - Email sans format valide (test@com).
    Vérifie que le système bloque la validation avec le message d'erreur approprié.
    """
    booking_page = BookingPage(driver)
    invalid_email = "amine.test@com" # Format invalide (manque le .com, .fr, etc.)

    # 1. Navigation jusqu'au formulaire
    driver.get(Config.BASE_URL)
    booking_page.click_book_now_nav()
    time.sleep(2)
    booking_page.expand_services_list()
    booking_page.select_first_service()
    time.sleep(1)
    booking_page.click_continue()
    booking_page.choose_first_available()
    booking_page.choose_first_available()
    booking_page.select_first_time()
    booking_page.click_continue()
    time.sleep(2)
    booking_page.click_continue() # Recurring
    time.sleep(3)

    # 2. Section Critique : Saisie de l'email invalide
    print(f"[ACTION] Saisie de l'email invalide : {invalid_email}")
    # On utilise fill_guest_info mais avec l'email erroné
    booking_page.fill_guest_info("Amine", "Abbes", invalid_email, "none")
    booking_page.fill_phone("55123456") # Phone valide pour isoler l'erreur email
    
    time.sleep(3) # Pause pour voir la saisie

    # 3. Tentative de validation
    booking_page.click_continue_or_book()
    
    # Pause critique pour voir l'apparition du message d'erreur rouge
    print("[WAIT] Observation de la validation du champ Email...")
    time.sleep(4) 

    # 4. Vérification du message d'erreur
    error_text = booking_page.get_email_error()
    expected_error = "Please enter a valid email address"

    if error_text == expected_error:
        print(f"[SUCCESS] Le site a bloqué l'email. Message : {error_text}")
        time.sleep(2)
    else:
        print(f"[BUG DETECTED] L'email '{invalid_email}' a été accepté ou l'erreur est différente : {error_text}")
        time.sleep(5)
        pytest.fail(f"Validation Email échouée : '{invalid_email}' a été accepté sans l'erreur correcte.")

    print("\n[RÉSULTAT] TC11 validé : Le format Email est contrôlé.")