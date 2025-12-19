import pytest
import time
from pages.login_page import LoginPage
from pages.booking_page import BookingPage
from config.config import Config
from utils.data_generator import DataGenerator

def test_complete_booking_flow_connected(driver):
    login_page = LoginPage(driver)
    booking_page = BookingPage(driver)

    # 1. Connexion initiale
    driver.get(Config.LOGIN_URL)
    login_page.enter_email("abbesamine01@gmail.com")
    login_page.enter_password(DataGenerator.PASSWORD_UNIQUE)
    login_page.click_login_submit()
    time.sleep(5) 

    # 2. Navigation vers la page de réservation
    booking_page.click_book_now_nav()
    time.sleep(3)

    # 3. Déplier la liste et choisir le Service
    booking_page.expand_services_list()
    time.sleep(1)
    booking_page.select_first_service()
    time.sleep(2)

    # 4. Étape Extras -> Continue
    booking_page.click_continue()
    time.sleep(2)

    # 5. Choisir le Barber (Any Barber)
    booking_page.choose_first_available()
    time.sleep(2)

    # 6. Choisir la Location
    booking_page.choose_first_available()
    time.sleep(2)

    # 7. Sélection Date & Time (6:45)
    booking_page.select_first_time()
    time.sleep(1)
    booking_page.click_continue()
    time.sleep(2)

    # 8. Étape Recurring -> Continue
    booking_page.click_continue()
    time.sleep(2)

    # 9. Formulaire Allergies (Gestion intelligente)
    booking_page.fill_allergies("yes")
    time.sleep(2)

    # 10. Transition vers la fin (Continue OU Book Now)
    booking_page.click_continue_or_book()
    time.sleep(2)

    # 11. Tentative finale si le message de succès n'est pas encore là
    if not booking_page.is_booking_confirmed():
        booking_page.confirm_final_booking()

    # 12. Vérification finale du message de succès
    time.sleep(2)
    assert booking_page.is_booking_confirmed(), "ERREUR : La réservation n'a pas été confirmée."
    
    print("\n[RÉSULTAT] TC05 : Flux de réservation complet validé !")