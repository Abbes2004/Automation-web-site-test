import pytest
import time
from pages.booking_page import BookingPage
from config.config import Config
from utils.data_generator import DataGenerator

def test_guest_complete_booking_flow(driver):
    """
    TC06: Booking (Guest) - Flux complet sans connexion.
    Vérifie qu'un utilisateur anonyme peut réserver.
    """
    booking_page = BookingPage(driver)
    data = DataGenerator.GUEST_DATA

    # 1. Accès direct à la page de réservation (Guest)
    driver.get(Config.BASE_URL) # Accès page principale
    time.sleep(2)
    booking_page.click_book_now_nav()
    time.sleep(3)

    # 2. Déplier les services et choisir le premier
    booking_page.expand_services_list()
    time.sleep(1)
    booking_page.select_first_service()
    time.sleep(2)

    # 3. Étape Extras -> Continue
    booking_page.click_continue()
    time.sleep(2)

    # 4. Étape Barber -> Choose
    booking_page.choose_first_available()
    time.sleep(2)

    # 5. Étape Location -> Choose
    booking_page.choose_first_available()
    time.sleep(2)

    # 6. Étape Date & Time (Sélection du premier créneau)
    booking_page.select_first_time()
    time.sleep(1)
    booking_page.click_continue()
    time.sleep(2)

    # 7. Étape Recurring -> Continue
    booking_page.click_continue()
    time.sleep(2)

    # 8. Étape Customer Info (GUEST)
    booking_page.fill_guest_info(
        data["first_name"], 
        data["last_name"], 
        data["email"], 
        data["allergie"]
    )
    time.sleep(1)
    booking_page.click_continue_or_book()
    time.sleep(2)

    # 9. Confirmation finale (Si page Checkout)
    if not booking_page.is_booking_confirmed():
        booking_page.confirm_final_booking()

    # 10. Vérification du succès final
    time.sleep(5)
    assert booking_page.is_booking_confirmed(), "ERREUR : Le message 'Thank you' n'est pas apparu pour le Guest."
    
    print(f"\n[RÉSULTAT] TC06 réussi : Réservation Guest effectuée pour {data['first_name']}.")