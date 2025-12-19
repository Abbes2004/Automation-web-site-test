from selenium.webdriver.common.by import By
from .base_page import BasePage

class SignupPage(BasePage):
    # --- Locators (Sélecteurs robustes basés sur les placeholders) ---
    FIRST_NAME_FIELD = (By.XPATH, "//input[@placeholder='Enter first name']")
    LAST_NAME_FIELD = (By.XPATH, "//input[@placeholder='Enter last name']")
    EMAIL_FIELD = (By.XPATH, "//input[@placeholder='Enter email']")
    PASSWORD_FIELD = (By.XPATH, "//input[@placeholder='Enter password']")
    
    # Sélecteur pour le bouton Sign Up (cherche le texte à l'intérieur du span)
    SIGNUP_SUBMIT_BTN = (By.XPATH, "//button[span[text()='Sign Up']]")

    # --- Actions ---
    def enter_first_name(self, first_name):
        self.send_keys(self.FIRST_NAME_FIELD, first_name)

    def enter_last_name(self, last_name):
        self.send_keys(self.LAST_NAME_FIELD, last_name)

    def enter_email(self, email):
        self.send_keys(self.EMAIL_FIELD, email)

    def enter_password(self, password):
        self.send_keys(self.PASSWORD_FIELD, password)

    def click_signup_submit(self):
        self.click(self.SIGNUP_SUBMIT_BTN)

    def complete_signup(self, first_name, last_name, email, password):
        """
        Méthode utilitaire pour effectuer l'inscription complète 
        en un seul appel dans tes scripts de test.
        """
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_password(password)
        self.click_signup_submit()