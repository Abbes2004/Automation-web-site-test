from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class BookingPage(BasePage):
    # --- Locators (Sélecteurs HTML) ---
    BOOK_NOW_NAV_LINK = (By.XPATH, "//a[@href='/booking']")
    # Ciblage spécifique de la flèche des services via l'attribut data-v fourni
    EXPAND_SERVICES_BTN = (By.XPATH, "//i[@data-v-18ae33be]")
    
    CHOOSE_SERVICE_BTN = (By.XPATH, "(//button[span[text()='Choose']])[1]")
    CONTINUE_BTN = (By.XPATH, "//button[span[text()='Continue']]")
    CHOOSE_OPTION_BTN = (By.XPATH, "(//button[span[text()='Choose']])[1]")
    
    # Sélecteur pour le créneau horaire (6:45)
    FIRST_TIME_SLOT = (By.XPATH, "//div[contains(@class, 'booking-ts')]")
    
    # Sélecteur pour le champ allergies
    ALLERGIES_INPUT = (By.XPATH, "//input[contains(@placeholder, 'allergies')]")
    
    # Bouton final de confirmation
    FINAL_BOOK_NOW_BTN = (By.XPATH, "//button[span[text()='Book Now']]")
    
    # Message de succès final
    SUCCESS_CONFIRMATION = (By.XPATH, "//div[contains(text(), 'Thank you and come again!')]")
    # --- Locators supplémentaires pour Guest ---
    GUEST_FIRST_NAME = (By.XPATH, "//input[@placeholder='Enter first name']")
    GUEST_LAST_NAME = (By.XPATH, "//input[@placeholder='Enter last name']")
    GUEST_EMAIL = (By.XPATH, "//input[@placeholder='Enter email']")
    # --- Locators pour le téléphone et l'erreur ---
    GUEST_PHONE = (By.CSS_SELECTOR, "input.vti__input")
    PHONE_ERROR_MSG = (By.XPATH, "//div[@class='el-form-item__error' and contains(text(), 'valid phone number')]")
    # --- Locator pour l'erreur Email ---
    EMAIL_ERROR_MSG = (By.XPATH, "//div[@class='el-form-item__error' and contains(text(), 'valid email address')]")

    AVATAR_MENU = (By.CSS_SELECTOR, "button.header__content__primary__right__logged")
    LOGOUT_BTN = (By.XPATH, "//span[contains(@class, 'ui-dropdown-item__label') and contains(text(), 'Log Out')]")
    CUSTOMER_INFO_TITLE = (By.XPATH, "//h4[contains(text(), 'Customer Info')]")

    CONFIRMATION_PRICE = (By.CSS_SELECTOR, "h5.text-primary span") # Pour extraire "$55 /" ou "$55"
    # --- Actions Guest ---
    def fill_guest_info(self, first, last, email, allergies):
        """Remplit le formulaire pour un utilisateur non connecté."""
        print(f"[ACTION] Saisie des infos Guest : {first} {last}")
        self.send_keys(self.GUEST_FIRST_NAME, first)
        self.send_keys(self.GUEST_LAST_NAME, last)
        self.send_keys(self.GUEST_EMAIL, email)
        # On réutilise la logique intelligente pour les allergies
        self.fill_allergies(allergies)

    # --- Actions ---
    def click_book_now_nav(self):
        self.click(self.BOOK_NOW_NAV_LINK)

    def expand_services_list(self):
        """Déploie la liste des services si elle est cachée."""
        print("[ACTION] Déploiement de la liste des services...")
        try:
            element = self.driver.find_element(*self.EXPAND_SERVICES_BTN)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", element)
            print("[SUCCESS] Liste dépliée.")
        except Exception as e:
            print(f"[WARNING] Impossible de déplier (déjà ouvert ?) : {e}")

    def select_first_service(self):
        self.click(self.CHOOSE_SERVICE_BTN)

    def click_continue(self):
        self.click(self.CONTINUE_BTN)

    def choose_first_available(self):
        """Utilisé pour Barber et Location."""
        self.click(self.CHOOSE_OPTION_BTN)

    def select_first_time(self):
        self.click(self.FIRST_TIME_SLOT)

    def fill_allergies(self, text="yes"):
        """Remplit les allergies seulement si le champ est visible."""
        print("[ACTION] Vérification du champ allergies...")
        try:
            # Timeout court (3s) pour ne pas bloquer le test si absent
            wait = WebDriverWait(self.driver, 3)
            field = wait.until(EC.visibility_of_element_located(self.ALLERGIES_INPUT))
            field.send_keys(text)
            print(f"[INFO] Champ rempli avec : {text}")
        except:
            print("[INFO] Champ absent (Utilisateur récurrent).")

    def click_continue_or_book(self):
        """Gère la transition finale entre l'étape allergies et le paiement."""
        try:
            wait = WebDriverWait(self.driver, 3)
            # On tente d'abord de cliquer sur Continue
            btn = wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN))
            btn.click()
            print("[INFO] Clic sur 'Continue' réussi.")
        except:
            # Si pas de continue, on tente directement le Book Now final
            print("[INFO] Pas de bouton 'Continue', essai sur 'Book Now' final.")
            self.confirm_final_booking()

    def confirm_final_booking(self):
        try:
            self.click(self.FINAL_BOOK_NOW_BTN)
            print("[ACTION] Clic sur le bouton final Book Now.")
        except Exception:
            print("[ERROR] Bouton Book Now introuvable.")

    def is_booking_confirmed(self):
        return self.is_visible(self.SUCCESS_CONFIRMATION)
    
    def fill_phone(self, phone_number):
        print(f"[ACTION] Saisie du téléphone dans le champ VTI : {phone_number}")
        # On utilise self.click avant pour s'assurer que le focus est sur le champ
        self.click(self.GUEST_PHONE)
        self.send_keys(self.GUEST_PHONE, phone_number)

    def get_phone_error(self):
        """Récupère le texte de l'erreur du champ téléphone."""
        try:
            # On attend que l'erreur apparaisse après le clic sur continue
            wait = WebDriverWait(self.driver, 5)
            error_element = wait.until(EC.visibility_of_element_located(self.PHONE_ERROR_MSG))
            return error_element.text
        except:
            return None
        
    def get_email_error(self):
        """Récupère le texte de l'erreur du champ email."""
        try:
            wait = WebDriverWait(self.driver, 5)
            error_element = wait.until(EC.visibility_of_element_located(self.EMAIL_ERROR_MSG))
            return error_element.text
        except:
            return None