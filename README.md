# ISTQB Project – Tests logiciels automatisés

## Présentation du projet
Ce projet fait partie d’une pratique orientée ISTQB en tests logiciels.

Il se concentre sur la conception, l’implémentation et l’exécution de tests automatisés pour une application SaaS de réservation de services en ligne (Trafft).
L’objectif principal est de valider le comportement fonctionnel, la robustesse et la fiabilité de l’application en utilisant des techniques de tests automatisés.

## Objectifs du projet
* Appliquer les principes ISTQB dans un cas réel
* Concevoir des cas de test fonctionnels, négatifs et aux limites
* Automatiser l’exécution des tests avec Selenium WebDriver et PyTest
* Détecter et documenter les anomalies
* Améliorer la répétabilité et la couverture des tests

## Périmètre des tests
* Tests côté client (frontend)
* Validation du workflow de réservation
* Vérification de la saisie des données et des messages d’erreur
* Compatibilité multi-navigateurs
* Tests de charge et de concurrence

## Technologies et outils utilisés
* **Langage :** Python 3.11
* **Framework de test :** PyTest
* **Outil d’automatisation :** Selenium WebDriver
* **Pattern :** Page Object Model (POM)
* **IDE :** PyCharm / VS Code
* **Navigateurs :** Google Chrome, Firefox, Microsoft Edge

## Structure du projet
Le projet est organisé de manière modulaire pour faciliter l’automatisation des tests :

* **tests/ :** cas de tests automatisés
* **pages/ :** classes POM représentant chaque page de l’application
* **utils/ :** fonctions et helpers réutilisables
* **screenshots/ :** captures d’écran des anomalies et des tests
* **reports/ :** rapports d’exécution des tests
* **README.md :** documentation du projet
* **requirements.txt :** dépendances Python
* **pytest.ini :** configuration PyTest

## Comment exécuter les tests
1. Installer les dépendances Python
2. Lancer l’exécution des tests avec PyTest
3. Générer des rapports détaillés (HTML) pour chaque exécution

## Gestion des anomalies
Les bugs détectés sont documentés avec :
* ID du cas de test
* Description du problème
* Résultat attendu vs résultat obtenu
* Captures d’écran

Cette démarche permet de reproduire et de suivre efficacement les anomalies.

## Auteurs
* **Amine Abbes**
* **Med Bechir Torki**
* **Année universitaire :** 2025–2026