import pytest
from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.booking_page import BookingPage
from config.config import Config
from utils.data_generator import DataGenerator

def test_full_flow_chrome():
    # Instanciation via DriverFactory
    driver = DriverFactory.get_driver("chrome")
    try:
        login_page = LoginPage(driver)
        booking_page = BookingPage(driver)

        # Parcours mémorisé
        driver.get(Config.LOGIN_URL)
        login_page.login("zz@gmail.com", DataGenerator.PASSWORD_UNIQUE)
        
        booking_page.click_book_now_nav()
        booking_page.expand_services_list()
        booking_page.select_first_service()
        booking_page.click_continue()         # Extras
        booking_page.choose_first_available() # Barber
        booking_page.choose_first_available() # Location
        booking_page.select_first_time()      # Time slot
        booking_page.click_continue()
        booking_page.click_continue()         # Recurring
        booking_page.fill_allergies("yes")
        booking_page.click_continue_or_book()
        
        if not booking_page.is_booking_confirmed():
            booking_page.confirm_final_booking()

        assert booking_page.is_booking_confirmed(), "Le booking a échoué sur Chrome"
        print("[SUCCESS] TC16 : Flux complet validé sur Google Chrome.")
    
    finally:
        driver.quit()