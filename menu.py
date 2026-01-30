"""
Menu principal du jeu BlindRevolution.
Gère la navigation entre les différentes options du jeu.

"""

from tts import parler
from menu_musique import choisir_niveau, choisir_musique
from outils import stop
from jeu import lancer_jeu  # On importe lancer_jeu
from wifi_esp32 import tester_esp32

def menu_principal():
    # Verification connexion esp32
    parler("Vérification de la connexion des bracelets.")
    if not tester_esp32():
        parler("Un ou plusieurs bracelets ne sont pas connectés. Veuillez vérifier la connexion avant de lancer le jeu.")
        return
    parler("Connexion des bracelets réussie.")

    first_time = True
    while True: 
        if first_time:
            parler("Bienvenue dans BlindRevolution.") # introduction au jeu
            first_time = False

        # Menu principal
        parler (
            "Vous êtes dans le menu principal."
            "Pour jouer, appuyez sur 1. "
            "Pour consulter les règles du jeu, appuyez sur 2. "
            "Pour accéder aux paramètres, appuyez sur 3. "
            "Pour quitter le jeu à tout moment, appuyez sur Q. "
            "Pour répéter ce menu, appuyez sur 0."
        )

        print("1 - Jouer")
        print("2 - Règles")
        print("3 - Paramètres")
        print("Q - Quitter")
        print("0 - Répéter le menu")

        choix = input("Votre choix : ")
        stop(choix)

        if choix == "1":
            while True:
                niveau = choisir_niveau()
                if niveau is None:
                    break

                while True:
                    musique = choisir_musique(niveau)
                    if musique is None:
                        break

                    parler("Le jeu va commencer.")
                    print("Niveau :", niveau)
                    print("Musique :", musique)


                    action = lancer_jeu(musique, niveau)

                    if action == "rejouer":
                        continue  # rejoue la même musique

                    elif action == "niveau":
                        break  # retourne au choix du niveau

        elif choix == "2":
            parler("Les règles du jeu seront expliquées plus tard.")

        elif choix == "3":
            parler("Les paramètres seront disponibles plus tard.")

        elif choix == "0":
            continue

        else:
            parler("Choix invalide.")
