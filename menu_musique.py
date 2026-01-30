"""
Module de gestion du menu musique

"""
import os
from tts import parler
from outils import stop, repete, retour
from audio import jouer_extrait

BASE_MUSIC_PATH = "Musique"

# Choix du niveau

def choisir_niveau():
    while True:
        parler(
            "Choisissez un niveau. "
            "Appuyez sur 1, 2 ou 3. "
            "Appuyez sur 0 pour répéter ce menu. "
            "Appuyez sur B pour revenir au menu principal. "
            "Ou appuyez sur Q pour quitter."
        )

        print("1 - Niveau 1")
        print("2 - Niveau 2")
        print("3 - Niveau 3")
        print("0 - Répéter")
        print("B - Retour")
        print("Q - Quitter")

        choix = input("Votre choix : ")

        # Quitter
        stop(choix)

        # Répéter
        if repete(choix):
            continue

        # Retour menu principal
        if retour(choix):
            return None

        if choix in ["1", "2", "3"]:
            parler(f"Vous avez choisi le niveau {choix}. Voici les musiques disponibles.")
            return int(choix)

        parler("Choix invalide.")


# Choix de la musique

def choisir_musique(niveau):
    dossier = os.path.join(BASE_MUSIC_PATH, f"Niveau{niveau}")

    if not os.path.isdir(dossier):
        parler("Erreur. Le dossier de musiques est introuvable.")
        return None

    musiques = sorted([
        f for f in os.listdir(dossier)
        if f.lower().endswith(".mp3")
    ])

    if not musiques:
        parler("Aucune musique disponible pour ce niveau.")
        return None

    # PHASE 1 : écoute des extraits
    for i, fichier in enumerate(musiques):
        numero = i + 1
        chemin_audio = os.path.join(dossier, fichier)
        nom_musique = os.path.splitext(fichier)[0].replace("_", " ")

        parler(f"Choix numéro {numero}. {nom_musique}.")
        jouer_extrait(chemin_audio, duree=5)

    # PHASE 2 : choix de la musique
    while True:
        parler(
            "Appuyez sur le numéro de la musique que vous souhaitez. "
            "Appuyez sur zéro pour réécouter les extraits. "
            "Appuyez sur B pour revenir au choix du niveau. "
            "Ou appuyez sur Q pour quitter."
        )

        for i, fichier in enumerate(musiques):
            nom_musique = os.path.splitext(fichier)[0].replace("_", " ")
            print(f"{i+1} - {nom_musique}")

        print("0 - Réécouter les extraits")
        print("B - Retour")
        print("Q - Quitter")

        choix = input("Votre choix : ")

        # Quitter
        stop(choix)

        # Retour au choix du niveau
        if retour(choix):
            return None

        # Réécouter les extraits
        if choix == "0":
            return choisir_musique(niveau)

        # Choix valide
        if choix.isdigit():
            index = int(choix) - 1
            if 0 <= index < len(musiques):
                musique_choisie = musiques[index]
                chemin_audio = os.path.join(dossier, musique_choisie)
                nom_musique = os.path.splitext(musique_choisie)[0].replace("_", " ")

                parler(f"Vous avez choisi {nom_musique}.")
                return chemin_audio

        parler("Choix invalide.")