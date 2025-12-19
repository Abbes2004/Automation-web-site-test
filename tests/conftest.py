import pytest
import sys
import os

# 1. On ajoute la racine du projet au PATH pour que "from pages..." fonctionne
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.driver_factory import DriverFactory
from config.config import Config

@pytest.fixture(scope="function")
def driver():
    """Fixture qui crée le driver avant chaque test et le ferme après."""
    
    # On utilise les réglages de ton fichier config.py
    browser = Config.DEFAULT_BROWSER
    headless = Config.HEADLESS_MODE
    
    # Création du driver via la Factory
    driver = DriverFactory.get_driver(browser_name=browser, headless=headless)
    
    # On donne le driver au test
    yield driver
    
    # On ferme le navigateur à la fin
    driver.quit()