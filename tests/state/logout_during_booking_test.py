import pytest
import time
from pages.login_page import LoginPage
from pages.booking_page import BookingPage
from config.config import Config
from utils.data_generator import DataGenerator
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_logout_during_customer_info_flow(driver):
    """
    TC14: Déconnexion forcée pendant le formulaire client.
    Vérifie le passage en mode Guest après déconnexion.
    """
    login_page = LoginPage(driver)
    booking_page = BookingPage(driver)
    wait = WebDriverWait(driver, 15) # Augmentation du timeout pour la stabilité

    # 1. Login
    print("\n[STEP 1] Connexion à l'application...")
    driver.get(Config.LOGIN_URL)
    login_page.login("abbesamine01@gmail.com", DataGenerator.PASSWORD_UNIQUE)
    time.sleep(3)

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

    # 3. Vérification Customer Info
    print("[STEP 4] Arrivée sur 'Customer Info'...")
    time.sleep(3)
    assert booking_page.is_visible(booking_page.CUSTOMER_INFO_TITLE), "Titre 'Customer Info' non trouvé."

    # 4. LOGOUT FORCÉ
    print("[STEP 5] Déclenchement du Log Out...")
    try:
        # A. Clic sur l'avatar (déjà fonctionnel chez vous)
        avatar_button = wait.until(EC.presence_of_element_located(booking_page.AVATAR_MENU))
        driver.execute_script("arguments[0].click();", avatar_button)
        print("[INFO] Avatar cliqué, attente du menu...")
        
        # B. Attente que le menu soit injecté dans le DOM
        time.sleep(2)

        # C. Clic JS sur le bouton Log Out
        # On cherche le span qui contient 'Log Out' peu importe où il est dans la page
        js_logout = """
            let items = document.querySelectorAll('.ui-dropdown-item__label');
            for (let item of items) {
                if (item.innerText.includes('Log Out')) {
                    item.closest('.ui-dropdown-item__wrapper').click();
                    return true;
                }
            }
            return false;
        """
        success = driver.execute_script(js_logout)
        
        if success:
            print("[SUCCESS] Clic JavaScript effectué sur Log Out.")
        else:
            # Plan B: Tentative via Selenium standard si le JS ne trouve pas
            print("[RETRY] JS n'a pas trouvé, tentative via Selenium...")
            logout_el = wait.until(EC.element_to_be_clickable(booking_page.LOGOUT_BTN))
            logout_el.click()

    except Exception as e:
        pytest.fail(f"Impossible de finaliser la déconnexion : {e}")

    # 5. VÉRIFICATION FINALE (MODE GUEST)
    print("[STEP 6] Vérification du mode Guest (First Name visible)...")
    time.sleep(5) # Attente du refresh de la page

    if booking_page.is_visible(booking_page.GUEST_FIRST_NAME):
        print("[SUCCESS] TC14 : Le formulaire est bien passé en mode Guest.")
    else:
        # Si non visible, on tente un dernier check via JS
        is_guest = driver.execute_script("return document.querySelector('input[placeholder=\"Enter first name\"]') !== null;")
        if is_guest:
             print("[SUCCESS] TC14 : Détecté via JS (Mode Guest actif).")
        else:
             pytest.fail("Le champ First Name n'est pas apparu. La session est peut-être restée active.")