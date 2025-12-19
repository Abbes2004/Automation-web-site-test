import pytest
import time
from pages.booking_page import BookingPage
from config.config import Config

def test_phone_validation_vulnerability_alphanumeric(driver):
    """
    TC10: Faille de sécurité/validation - Téléphone Alphanumérique.
    Objectif : Vérifier si le système accepte des lettres dans le numéro.
    """
    booking_page = BookingPage(driver)
    vulnerability_payload = "ABCD1234"

    # 1. Navigation jusqu'au formulaire
    driver.get(Config.BASE_URL)
    booking_page.click_book_now_nav()
    time.sleep(2)
    booking_page.expand_services_list()
    booking_page.select_first_service()
    time.sleep(2) # Pause pour voir la sélection
    booking_page.click_continue()
    booking_page.choose_first_available()
    booking_page.choose_first_available()
    booking_page.select_first_time()
    booking_page.click_continue()
    time.sleep(2)
    booking_page.click_continue()
    time.sleep(3) # Attente pour l'affichage de la page Customer Info

    # 2. Section Critique : Saisie des données
    print(f"[ACTION] Test de faille : Injection de '{vulnerability_payload}'...")
    booking_page.fill_guest_info("Amine", "Abbes", "bug.report@test.com", "none")
    
    # On marque une pause pour voir le champ téléphone avant saisie
    time.sleep(2)
    booking_page.fill_phone(vulnerability_payload)
    
    # Pause pour bien voir la valeur 'ABCD1234' écrite dans le champ
    time.sleep(4) 

    # 3. Tentative de validation
    booking_page.click_continue_or_book()
    
    # On laisse 5 secondes pour observer si le site change de page ou affiche une erreur
    print("[WAIT] Observation du comportement du site...")
    time.sleep(5) 

    # 4. Analyse du résultat
    error_text = booking_page.get_phone_error()

    if error_text is None:
        # Si aucune erreur n'est trouvée, le site a accepté la valeur (BUG)
        print(f"\n[BUG DETECTED] Le site a accepté le numéro '{vulnerability_payload}' et est passé à l'étape suivante !")
        
        # Pause finale avant fermeture pour prendre une photo/capture d'écran si besoin
        time.sleep(5)
        
        # On force le FAIL pour le rapport car c'est un comportement anormal
        pytest.fail(f"FAILLE VALIDÉE : Le téléphone '{vulnerability_payload}' a été accepté.")
    else:
        # Si une erreur est trouvée, le bug est corrigé
        print(f"\n[SUCCESS] Le site a bloqué la saisie. Message : {error_text}")
        print("[INFO] La faille a été corrigée.")
        time.sleep(3)