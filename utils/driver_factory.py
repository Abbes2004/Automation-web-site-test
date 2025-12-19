# utils/driver_factory.py simplifié
from selenium import webdriver

class DriverFactory:
    @staticmethod
    def get_driver(browser_name="chrome", headless=False):
        browser = browser_name.lower()

        if browser == "chrome":
            options = webdriver.ChromeOptions()
            if headless: options.add_argument("--headless")
            options.add_argument("--start-maximized")
            # Plus besoin de Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(options=options)

        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            if headless: options.add_argument("-headless")
            driver = webdriver.Firefox(options=options)

        elif browser == "edge":
            options = webdriver.EdgeOptions()
            if headless: options.add_argument("--headless")
            # Selenium 4 s'occupe de trouver le msedgedriver automatiquement
            driver = webdriver.Edge(options=options)

        else:
            raise ValueError(f"Navigateur '{browser_name}' non supporté.")

        driver.implicitly_wait(10)
        return driver