from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    # --- Locators ---
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.ui-button .ui-icon-login")
    SERVICES_LINK = (By.XPATH, "//a[contains(text(), 'Services')]")
    BARBERS_LINK = (By.XPATH, "//a[contains(text(), 'Barbers')]")
    BOOK_NOW_NAV = (By.XPATH, "//a[contains(@href, '/booking')]") # Dans la barre de nav
    
    # Le gros bouton "Book Now" au centre de l'image
    MAIN_BOOK_NOW_BTN = (By.XPATH, "//button[span[text()='Book Now']]")
    
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search services']")
    
    # Filtres
    CATEGORIES_FILTER = (By.XPATH, "//div[text()='Categories']")
    FILTER_BARBERSHOP = (By.XPATH, "//div[text()='Barbershop']")
    
    # Éléments d'une carte de service (le premier trouvé par exemple)
    SERVICE_CARD_BOOK_BTN = (By.CSS_SELECTOR, ".ui-button__type__primary")

    # --- Actions ---
    def go_to_booking(self):
        self.click(self.MAIN_BOOK_NOW_BTN)

    def search_service(self, service_name):
        self.send_keys(self.SEARCH_INPUT, service_name)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)
        
    def filter_by_barbershop(self):
        self.click(self.CATEGORIES_FILTER)
        self.click(self.FILTER_BARBERSHOP)