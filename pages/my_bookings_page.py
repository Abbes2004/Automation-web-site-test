from selenium.webdriver.common.by import By
from .base_page import BasePage
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MyBookingsPage(BasePage):
    
    # --- Locators ---
    # Le bouton "..." (Options) sur le premier rendez-vous de la liste
    OPTIONS_BTN = (By.XPATH, "(//i[contains(@class, 'ui-icon-more-options')])[1]")
    """# On définit le locator pour TOUS les boutons d'options
    ALL_OPTIONS_BTNS = (By.CSS_SELECTOR, "button .ui-icon-more-options")
    # Bouton Cancel (on attend qu'il soit visible dans le menu déroulant)
    CANCEL_BTN = (By.XPATH, "//li[contains(@class, 'el-dropdown-menu__item')]//span[text()='Cancel'] | //button[span[text()='Cancel']]")
    # Modale de confirmation d'annulation
    CONFIRM_CANCEL_BTN = (By.XPATH, "//button[contains(@class, 'ui-button__type__warning') and .//span[contains(text(), 'Confirm Cancellation')]]")"""

    # Cible tous les boutons "..."
    ALL_OPTIONS_BTNS = (By.CSS_SELECTOR, "button .ui-icon-more-options")

    # Cible le bouton Cancel du menu
    CANCEL_BTN = (By.XPATH, "//li[contains(@class, 'el-dropdown-menu__item')]//span[contains(text(), 'Cancel')]")

    # Cible le bouton de confirmation par son texte exact (très robuste)
    # On cherche un bouton qui contient exactement le span avec le texte
    CONFIRM_CANCEL_BTN = (By.XPATH, "//button[.//span[text()='Confirm Cancellation']]")

    DISCARD_BTN = (By.XPATH, "//button[span[text()='Discard']]")
    
    # Messages de succès
    MSG_CANCELED_SUCCESS = (By.XPATH, "//h2[text()='Booking Has Been Canceled']")
    MSG_RESCHEDULED = (By.XPATH, "//h2[text()='Booking Has Been Rescheduled']")
    # L'ANOMALIE : Message quand le site se trompe de RDV
    MSG_ALREADY_CANCELED = (By.XPATH, "//h2[text()='Booking Already Canceled']")

    # Informations du RDV (Pour vérification)
    SERVICE_TITLE = (By.XPATH, "//h6") # Le titre du service dans la carte

    # On cible l'icône "..." du DERNIER rendez-vous affiché
    LAST_OPTIONS_BTN = (By.XPATH, "(//div[contains(@class, 'my-bk__body__data__date__appointments__item')])[last()]//i[contains(@class, 'ui-icon-more-options')]")

    NO_SLOTS_MSG = (By.XPATH, "//h5[contains(text(), 'No timeslots available')]")

    """ # Bouton Reschedule (on attend qu'il soit visible dans le menu déroulant)
    RESCHEDULE_BTN = (By.XPATH, "//button[span[text()='Reschedule']]")
    
    STATUS_APPROVED = (By.XPATH, "//span[contains(text(), 'Approved')]")
    # Bouton final dans la fenêtre de changement de date
    FINAL_RESCHEDULE_BTN = (By.XPATH, "//button[.//span[text()='Reschedule']]")"""

    # Cible le texte "Reschedule" à l'intérieur de la liste déroulante
   # Cible le span spécifique que vous avez identifié
    RESCHEDULE_BTN = (By.XPATH, "//span[@class='ui-dropdown-item__label par-sm' and text()='Reschedule']")

    # Status "Approved" pour être sûr de cliquer sur un RDV valide
    STATUS_APPROVED = (By.XPATH, "//span[text()='Approved']")

    # Cible exactement le bouton avec le texte Reschedule (insensible aux data-v-xxxx)
    FINAL_RESCHEDULE_BTN = (By.XPATH, "//button[contains(@class, 'ui-button__type__primary')]//span[text()='Reschedule']")
    # XPath pour le deuxième créneau horaire s'il existe, sinon le premier
    SECOND_TIME_SLOT = (By.XPATH, "(//div[contains(@class, 'time-slot')])[2] | (//div[contains(@class, 'time-slot')])[1]")

    # Cible un créneau horaire qui n'est PAS actif (donc un différent du actuel)
    DIFFERENT_TIME_SLOT = (By.XPATH, "//div[contains(@class, 'booking-ts') and not(contains(@class, 'is-active'))]")

    # Dans pages/my_bookings_page.py
    MSG_UNABLE_TO_RESCHEDULE = (By.XPATH, "//h2[contains(text(), 'Unable to Reschedule Booking')]")

    LAST_BOOKING_ITEM = (By.CSS_SELECTOR, ".my-bk__body__data__date__appointments__item")
    DETAIL_TOTAL_PRICE = (By.XPATH, "//div[contains(@class, 'flex-col')]//h5[contains(text(), '$')]")

    # Le bouton que tu as décrit (toutes résolutions)
    BOOK_NOW_SPAN = (By.XPATH, "//span[normalize-space()='Book Now']")
    # --- Actions ---

    def open_options_for_first_booking(self):
        """Ouvre le menu '...' du premier booking de la liste."""
        # On attend que la liste charge
        time.sleep(1) 
        self.click(self.OPTIONS_BTN)

    def cancel_process(self):
        """Processus d'annulation sur le dernier élément de la liste."""
        print("[ACTION] Tentative d'annulation du dernier booking...")
        time.sleep(3) # Attente du chargement complet de la liste
        
        # 1. Cliquer sur les points de suspension du dernier item
        self.click(self.LAST_OPTIONS_BTN)
        print("[INFO] Menu options ouvert.")
        time.sleep(1.5)
        
        # 2. Cliquer sur Cancel (avec un clic JS pour éviter les problèmes de menu flottant)
        cancel_el = self.find_element(self.CANCEL_BTN)
        self.driver.execute_script("arguments[0].click();", cancel_el)
        print("[INFO] Bouton Cancel cliqué.")
        time.sleep(1.5)
        
        # 3. Confirmer l'annulation
        self.click(self.CONFIRM_CANCEL_BTN)
        print("[INFO] Confirmation envoyée.")

    def reschedule_booking(self):
        """Ouvre les options et clique sur Reschedule via JavaScript."""
        self.open_options_for_first_booking()
        print("[ACTION] Clic sur l'option Reschedule du menu...")
        time.sleep(2)
        
        try:
            # On cherche le span que vous avez mentionné
            reschedule_el = self.find_element(self.RESCHEDULE_BTN)
            self.driver.execute_script("arguments[0].click();", reschedule_el)
        except:
            # Backup : recherche par texte brut si le chemin XPATH échoue
            self.driver.execute_script("document.evaluate(\"//span[text()='Reschedule']\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")
    
    def open_last_booking_options(self):
        """Ouvre le menu '...' du rendez-vous le plus récent."""
        print("[ACTION] Ouverture des options du dernier booking...")
        time.sleep(2) # Attente du chargement de la liste
        self.click(self.OPTIONS_BTN)

    def cancel_process(self):
        """Action pour annuler systématiquement le rendez-vous le plus bas."""
        print("[ACTION] Tentative d'annulation du booking le plus bas dans la liste...")
        time.sleep(3) # Attente indispensable pour le chargement du DOM
        
        # 1. Cliquer sur les options du dernier élément
        # On utilise un scroll avant pour être sûr que l'élément est dans la vue
        options_element = self.find_element(self.LAST_OPTIONS_BTN)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", options_element)
        time.sleep(1)
        self.click(self.LAST_OPTIONS_BTN)
        print("[INFO] Menu options du dernier booking ouvert.")
        
        # 2. Cliquer sur le bouton Cancel (souvent dans un calque el-dropdown)
        time.sleep(1.5)
        cancel_el = self.find_element(self.CANCEL_BTN)
        # On utilise un clic JavaScript car les menus ElementUI sont parfois capricieux
        self.driver.execute_script("arguments[0].click();", cancel_el)
        print("[INFO] Bouton 'Cancel' cliqué.")
        
        # 3. Confirmer l'annulation
        time.sleep(1.5)
        self.click(self.CONFIRM_CANCEL_BTN)
        print("[INFO] Confirmation envoyée.")
    # --- Vérifications ---

    def cancel_last_booking(self):
        #Méthode mixée : Trouve le dernier booking ET force la confirmation.
        print("[ACTION] Localisation du dernier booking dans la liste...")
        time.sleep(3) 

        # --- PARTIE 1 : TROUVER LE DERNIER BOOKING ---
        # On récupère tous les boutons d'options
        elements = self.driver.find_elements(*self.ALL_OPTIONS_BTNS)
        if not elements:
            print("[ERREUR] Aucun booking trouvé sur la page.")
            return False
        
        # On prend le dernier de la liste
        last_booking_btn = elements[-1]
        
        # Scroll et clic
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", last_booking_btn)
        time.sleep(1)
        last_booking_btn.click()
        print("[INFO] Menu du dernier booking ouvert.")

        # --- PARTIE 2 : CLIC SUR CANCEL ---
        time.sleep(2)
        try:
            cancel_el = self.find_element(self.CANCEL_BTN)
            self.driver.execute_script("arguments[0].click();", cancel_el)
            print("[INFO] Option 'Cancel' sélectionnée.")
        except:
            # Backup si le premier sélecteur échoue
            self.driver.execute_script("document.querySelector('.el-dropdown-menu__item i.ui-icon-close')?.parentElement.click();")

        # --- PARTIE 3 : CONFIRMATION DANS LA MODALE ---
        print("[ACTION] Tentative de confirmation...")
        time.sleep(2) # Attente de l'apparition de la modale
        
        try:
            # On utilise le driver direct pour contourner les attentes de base_page
            confirm_btn = self.driver.find_element(*self.CONFIRM_CANCEL_BTN)
            self.driver.execute_script("arguments[0].click();", confirm_btn)
            print("[SUCCESS] Booking annulé avec succès.")
        except Exception as e:
            print(f"[CRITIQUE] Le bouton de confirmation est introuvable par Selenium.")
            # Solution de secours ultime : cliquer sur n'importe quel bouton 'warning' dans une modale
            self.driver.execute_script("document.querySelector('.ui-button__type__warning').click();")

    # --- Vérifications ---
    def check_status_canceled(self):
        return self.is_visible(self.MSG_CANCELED_SUCCESS)

    def check_anomaly_detected(self):
        """Vérifie si le bug 'Already Canceled' apparaît."""
        return self.is_visible(self.MSG_ALREADY_CANCELED)

    def is_booking_approved(self):
        return self.is_visible(self.STATUS_APPROVED)
    
    def confirm_reschedule(self):
        """Clique sur le bouton Reschedule orange de la page de calendrier."""
        btn = self.find_element(self.FINAL_RESCHEDULE_BTN)
        self.driver.execute_script("arguments[0].click();", btn)

    def is_reschedule_success(self):
        """Vérifie si le message de succès est affiché."""
        return self.is_visible(self.MSG_RESCHEDULED)
    
    def reschedule_last_booking(self):
        """Cible le dernier booking et force le clic sur l'option Reschedule."""
        print("[ACTION] Recherche du dernier booking...")
        time.sleep(3)
        elements = self.driver.find_elements(*self.ALL_OPTIONS_BTNS)
        
        if not elements:
            raise Exception("Aucun booking trouvé.")
            
        last_item = elements[-1]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", last_item)
        time.sleep(1)
        last_item.click()
        print("[INFO] Menu options ouvert.")
        
        # --- LA CORRECTION ICI ---
        print("[ACTION] Tentative de clic sur le span 'Reschedule'...")
        time.sleep(1.5) # Attente que le menu soit déployé
        
        try:
            # On cherche l'élément Reschedule
            reschedule_span = self.driver.find_element(*self.RESCHEDULE_BTN)
            
            # On force le clic sur le span via JS pour ignorer les superpositions de calques
            self.driver.execute_script("arguments[0].click();", reschedule_span)
            print("[SUCCESS] Clic JavaScript effectué sur Reschedule.")
            
        except Exception as e:
            print(f"[RETRY] Echec du clic direct, tentative via texte brut : {e}")
            # Solution de secours ultime : cherche n'importe quel span qui contient 'Reschedule'
            self.driver.execute_script(
                "document.querySelectorAll('span').forEach(s => { if(s.innerText.includes('Reschedule')) s.click(); });"
            )

    def __init__(self, driver):
        self.driver = driver
        # On définit une attente explicite
        self.wait = WebDriverWait(driver, 15)

    def click_book_now_main(self):
        print("[DEBUG] Tentative de localisation du bouton Book Now...")
        try:
            # Utilisation du nom de méthode correct
            span_element = self.wait.until(EC.element_to_be_clickable(self.BOOK_NOW_SPAN))
            
            # On remonte au parent <button>
            button_element = span_element.find_element(By.XPATH, "./ancestor::button")

            # On s'assure que le bouton est bien dans le champ de vision (scroll)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_element)
            
            # Clic via JavaScript (plus fiable sur l'émulation mobile)
            self.driver.execute_script("arguments[0].click();", button_element)
            print("[DEBUG] Clic JavaScript effectué avec succès sur le bouton Book Now.")
            
        except Exception as e:
            print(f"[ERROR] Échec lors du clic sur le bouton : {str(e)}")
            self.driver.save_screenshot("error_responsive_click.png")
            raise e