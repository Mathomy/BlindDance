"""
Module pour la gestion des effets sonores dans le jeu.

"""

import pygame
import time

pygame.mixer.init()


# Chargement des effets
SON_SUCCESS = pygame.mixer.Sound("Sound_Effect/success.mp3")
SON_SUCCESS.set_volume(6.0)
SON_ERROR = pygame.mixer.Sound("Sound_Effect/error.mp3")
SON_STAR = pygame.mixer.Sound("Sound_Effect/star.mp3")

# Fonction pour jouer un extrait audio
def jouer_extrait(chemin_fichier, duree=5):
    """
    Joue un extrait audio pendant `duree` secondes
    """
    try:
        pygame.mixer.music.load(chemin_fichier)
        pygame.mixer.music.play()
        time.sleep(duree)
        pygame.mixer.music.stop()
    except Exception as e:
        print("Erreur audio :", e)

# Fonctions pour jouer des effets spécifiques
def jouer_succes():
    SON_SUCCESS.play()

def jouer_erreur():
    SON_ERROR.play()

def jouer_etoile():
    SON_STAR.play()
