"""
Outils pour les menus : gestion des choix utilisateur
"""

import sys
from tts import parler

# Fonction stop du jeu
def stop(choix):
    if choix.lower() == "q":
        parler("Merci d'avoir joué à BlindDance. À bientôt.")
        sys.exit(0)

# Fonction répéter le menu
def repete(texte):
    """
    Retourne True si on doit répéter le menu (touche 0),
    sinon False.
    Quitte si Q/q
    """
    if texte.lower() == "q":
        stop("q")
    elif texte == "0":
        return True
    return False

# Fonction retour au menu précédent
def retour(choix):
    """
    Retourne True si l'utilisateur demande
    un retour au menu précédent (touche B/b).
    Quitte si Q/q.
    """
    if choix.lower() == "q":
        stop("q")
    if choix.lower() == "b":
        return True
    return False
