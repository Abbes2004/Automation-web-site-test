from selenium.webdriver.common.by import By
import time
from .base_page import BasePage

class LoginPage(BasePage):
    EMAIL_FIELD = (By.XPATH, "//input[@placeholder='Enter email']")
    PASSWORD_FIELD = (By.XPATH, "//input[@placeholder='Enter password']")
    # On utilise un sélecteur plus large pour être sûr
    LOGIN_SUBMIT_BTN = (By.XPATH, "//button[.//span[contains(text(), 'Log In')]]")
    ERROR_MESSAGE = (By.CLASS_NAME, "ui-alert")
    SIGNUP_LINK = (By.XPATH, "//span[contains(text(), 'Sign Up now')]")

    def enter_email(self, email):
        self.send_keys(self.EMAIL_FIELD, email)

    def enter_password(self, password):
        self.send_keys(self.PASSWORD_FIELD, password)

    def click_login_submit(self):
        # On essaie un clic JavaScript si le clic normal échoue silencieusement
        element = self.find_element(self.LOGIN_SUBMIT_BTN)
        self.driver.execute_script("arguments[0].click();", element)
        print("Clic JavaScript effectué sur le bouton Log In")

    def get_error_message(self):
        """Retourne le texte de l'alerte d'erreur s'il est présent"""
        try:
            # On utilise find_element directement via base_page
            element = self.find_element(self.ERROR_MESSAGE)
            text = element.text
            print(f"[DEBUG] Texte trouvé dans l'alerte : {text}")
            return text
        except:
            return None
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_submit()
        # Attente implicite pour la redirection après login
        time.sleep(3)

    def go_to_signup(self):
        """Clique sur le lien 'Sign Up now' pour changer de formulaire."""
        print("[ACTION] Navigation vers le formulaire d'inscription...")
        # On utilise le clic JavaScript pour être sûr de passer outre d'éventuels overlays
        try:
            element = self.find_element(self.SIGNUP_LINK)
            self.driver.execute_script("arguments[0].click();", element)
        except:
            # Si le span n'est pas cliquable directement, on clique sur son parent (le lien/bouton)
            element = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Sign Up now')]/..")
            self.driver.execute_script("arguments[0].click();", element)
