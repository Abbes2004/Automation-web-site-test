from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class WaitUtils:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_visibility(self, locator):
        """Attend que l'élément soit présent dans le DOM et visible."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print(f"Erreur : L'élément {locator} n'est pas devenu visible après le délai.")
            return None

    def wait_for_clickable(self, locator):
        """Attend que l'élément soit cliquable (visible et activé)."""
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            print(f"Erreur : L'élément {locator} n'est pas cliquable.")
            return None

    def wait_for_presence(self, locator):
        """Attend que l'élément soit présent dans le DOM (pas forcément visible)."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_invisibility(self, locator):
        """Attend que l'élément disparaisse (utile pour les spinners/chargements)."""
        return self.wait.until(EC.invisibility_of_element_located(locator))