import random
import string

class DataGenerator:
    # --- Comptes existants ---
    EXISTING_ACCOUNTS = [
        "abbesamine01@gmail.com",
        "abbesamine02@gmail.com",
        "abbesamine03@gmail.com",
        "abbesamine04@gmail.com",
        "abbesamine05@gmail.com"
    ]
    PASSWORD_UNIQUE = "aaabbbccc"

    # --- Infos Guest ---
    GUEST_DATA = {
        "first_name": "amine",
        "last_name": "abbes",
        "email": "guest.amine@test.com",
        "allergie": "yes"
    }

    # --- Données de Limites (BVA) ---
    # Ta chaîne de 255 caractères exacte
    LONG_NAME = "abcde" * 51 
    TOO_LONG_NAME = "A" * 256  # 256 caractères

    # --- Données pour Thread / Concurrence (TC21) ---
    BOOKING_CONCURRENCY = {
        "service": "Shaving the head",
        "barber": "Benjamin Martinez",
        "date": "20", # Le jour du mois (Saturday 20)
        "time": "1:00" # Heure de début
    }

    # --- Générateurs dynamiques ---
    @staticmethod
    def generate_random_email():
        """Génère un email unique pour le test de Sign-up (TC01)."""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"testuser_{random_str}@gmail.com"

    @staticmethod
    def get_existing_account(index=0):
        """Récupère un des comptes de la liste."""
        if index < len(DataGenerator.EXISTING_ACCOUNTS):
            return DataGenerator.EXISTING_ACCOUNTS[index]
        return DataGenerator.EXISTING_ACCOUNTS[0]