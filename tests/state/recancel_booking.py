import pytest
import time
from pages.login_page import LoginPage
from pages.booking_page import BookingPage
from pages.my_bookings_page import MyBookingsPage
from config.config import Config
from utils.data_generator import DataGenerator

def test_double_booking_cancellation_anomaly(driver):
    """
    TC12: Transition d'États - Confusion Double Booking.
    Vérifie si le système annule le bon RDV après une ré-réservation.
    """
    login_page = LoginPage(driver)
    booking_page = BookingPage(driver)
    my_bk_page = MyBookingsPage(driver)

    # 1. Connexion
    driver.get(Config.LOGIN_URL)
    login_page.login("zz@gmail.com", DataGenerator.PASSWORD_UNIQUE)
    time.sleep(3)

    # --- CYCLE 1 : PREMIER BOOKING ---
    print("\n--- CYCLE 1 : Réservation et Annulation ---")
    driver.get(f"{Config.BASE_URL}/booking") # Accès direct
    time.sleep(2)
    booking_page.expand_services_list()
    booking_page.select_first_service()
    booking_page.click_continue() # Extras
    booking_page.choose_first_available() # Barber
    booking_page.choose_first_available() # Location
    booking_page.select_first_time()
    booking_page.click_continue()
    booking_page.click_continue() # Recurring
    booking_page.fill_allergies("none")
    booking_page.click_continue_or_book()
    time.sleep(3)
    if not booking_page.is_booking_confirmed(): booking_page.confirm_final_booking()
    
    # Annulation du Cycle 1
    driver.get(f"{Config.BASE_URL}/my-bookings")
    my_bk_page.cancel_last_booking()
    time.sleep(3)
    assert my_bk_page.check_status_canceled(), "ERREUR : Le premier RDV n'a pas été annulé."
    print("[SUCCESS] Premier RDV annulé correctement.")

    # --- CYCLE 2 : RE-BOOKING DU MÊME SERVICE ---
    print("\n--- CYCLE 2 : Nouveau Booking identique ---")
    driver.get(f"{Config.BASE_URL}/booking")
    time.sleep(2)
    booking_page.expand_services_list()
    booking_page.select_first_service()
    booking_page.click_continue()
    booking_page.choose_first_available()
    booking_page.choose_first_available()
    booking_page.select_first_time()
    booking_page.click_continue()
    booking_page.click_continue()
    booking_page.fill_allergies("none")
    booking_page.click_continue_or_book()
    time.sleep(3)
    if not booking_page.is_booking_confirmed(): booking_page.confirm_final_booking()

    # Tentative d'annulation du Cycle 2 (Détection du Bug)
    print("\n[ACTION] Tentative d'annulation du second RDV...")
    driver.get(f"{Config.BASE_URL}/my-bookings")
    time.sleep(2)
    my_bk_page.cancel_last_booking()
    time.sleep(4) # Pause critique pour voir le message d'erreur

    # ANALYSE DE L'ANOMALIE
    if my_bk_page.check_anomaly_detected():
        print("[BUG DETECTED] Message 'Booking Already Canceled' apparu !")
        time.sleep(5) # Laisser le temps de voir l'erreur à l'écran
        pytest.fail("ANOMALIE TC12 : Le système tente d'annuler un RDV déjà annulé au lieu du nouveau.")
    else:
        print("[SUCCESS] Le second RDV a été annulé sans erreur.")
        time.sleep(2)