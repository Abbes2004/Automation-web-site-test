import threading
import pytest
import time
from concurrent.futures import ThreadPoolExecutor
from utils.driver_factory import DriverFactory
from utils.data_generator import DataGenerator
from pages.login_page import LoginPage
from pages.booking_page import BookingPage
from config.config import Config

# Barrière pour bloquer les 5 threads jusqu'à ce qu'ils soient tous au même point
sync_barrier = threading.Barrier(5)
results = []

def execute_concurrent_booking(email):
    driver = DriverFactory.get_driver("chrome")
    driver.maximize_window()
    
    login_page = LoginPage(driver)
    booking_page = BookingPage(driver)
    
    thread_info = {"email": email, "outcome": "FAILED", "msg": ""}

    try:
        # 1. Login
        driver.get(Config.LOGIN_URL)
        login_page.login(email, DataGenerator.PASSWORD_UNIQUE)
        time.sleep(2)

        # 2. Déroulement du chemin fourni
        booking_page.click_book_now_nav()
        booking_page.expand_services_list()
        booking_page.select_first_service()
        booking_page.click_continue()          # Étape Extras
        
        booking_page.choose_first_available()  # Sélection Barber
        booking_page.choose_first_available()  # Sélection Location
        
        booking_page.select_first_time()       # Sélection du Time slot
        booking_page.click_continue()
        
        booking_page.click_continue()          # Étape Recurring
        booking_page.fill_allergies("yes")

        # --- POINT DE SYNCHRONISATION CRITIQUE ---
        print(f"[THREAD {email}] Prêt pour le clic final. Attente des autres...")
        sync_barrier.wait() 
        # ------------------------------------------

        # 3. Tentative de réservation finale
        booking_page.click_continue_or_book()
        
        # Sécurité supplémentaire demandée : si non confirmé, on tente le bouton final
        time.sleep(1)
        if not booking_page.is_booking_confirmed():
            booking_page.confirm_final_booking()

        # 4. Analyse du résultat après un court délai de traitement serveur
        time.sleep(5)
        if booking_page.is_booking_confirmed():
            thread_info["outcome"] = "SUCCESS"
            thread_info["msg"] = "Réservation réussie (Gagnant)"
        else:
            thread_info["outcome"] = "REJECTED"
            thread_info["msg"] = "Réservation rejetée (Conflit de créneau)"

    except Exception as e:
        thread_info["msg"] = f"Erreur technique : {str(e)}"
    finally:
        results.append(thread_info)
        driver.quit()

def test_tc21_concurrency_race_condition():
    emails = DataGenerator.EXISTING_ACCOUNTS[:5] # Vos 5 emails
    
    print(f"\n[START] Lancement du test de concurrence sur 5 threads...")
    
    # Utilisation de ThreadPoolExecutor pour lancer les 5 drivers en parallèle
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(execute_concurrent_booking, emails)

    # --- Analyse des résultats finaux ---
    success_list = [r for r in results if r["outcome"] == "SUCCESS"]
    rejected_list = [r for r in results if r["outcome"] == "REJECTED"]

    print("\n" + "="*50)
    print("RÉSULTATS DU TEST DE CONCURRENCE")
    print("="*50)
    for res in results:
        print(f"Utilisateur: {res['email']} | Résultat: {res['outcome']} | Message: {res['msg']}")

    # ASSERTIONS ISTQB / QUALITÉ
    # 1. On vérifie qu'il y a exactement 1 succès
    assert len(success_list) == 1, f"ALERTE : {len(success_list)} succès détectés au lieu de 1 ! Risque d'overbooking."
    
    # 2. On vérifie que les 4 autres sont rejetés
    assert len(rejected_list) == 4, f"ALERTE : {len(rejected_list)} rejets au lieu de 4."

    print("\n[FINAL] Test réussi : Le système a correctement géré le conflit de créneau.")