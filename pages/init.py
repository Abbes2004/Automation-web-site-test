# pages/__init__.py

# On importe les classes depuis leurs fichiers respectifs pour un accès simplifié
from .base_page import BasePage
from .home_page import HomePage
from .login_page import LoginPage
# Ce fichier contient maintenant toute la logique du flux de réservation (Services, Calendrier, Formulaire)
from .booking_page import BookingPage
# Ce fichier gère l'historique, l'annulation et le report des rendez-vous
from .my_bookings_page import MyBookingsPage

# On expose les classes pour permettre l'import direct : from pages import HomePage, BookingPage, etc.
__all__ = [
    "BasePage",
    "HomePage",
    "LoginPage",
    "BookingPage",
    "MyBookingsPage"
]