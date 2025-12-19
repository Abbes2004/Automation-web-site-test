import time

class PerformanceUtils:
    """
    Outil pour mesurer le temps d'exécution des actions de test.
    Utile pour valider les SLAs (ex: chargement < 2s).
    """

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.duration = None

    def __enter__(self):
        """Démarre le chronomètre au début du bloc 'with'."""
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Arrête le chronomètre à la fin du bloc 'with'."""
        self.end_time = time.perf_counter()
        self.duration = self.end_time - self.start_time
        # On affiche le résultat (on pourra plus tard l'envoyer vers un logger ou un fichier Excel)
        print(f"\n[PERF] Action terminée en : {self.duration:.4f} secondes")

    @staticmethod
    def measure_action(func, *args, **kwargs):
        """
        Méthode statique simple pour mesurer une fonction spécifique.
        """
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[PERF] Fonction {func.__name__} exécutée en {end - start:.4f}s")
        return result