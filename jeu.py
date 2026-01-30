"""
Module principal du fonctionnement du jeu.

"""


import time
import pygame
from tts import parler
from audio import jouer_succes, jouer_erreur, jouer_etoile
import librosa
import requests
from threading import Thread
import random
import wifi_esp32

# IP des ESP32 connectés
ESP32_CONFIG = [
    wifi_esp32.IP_S3,  # ESP32 S3
    wifi_esp32.IP_C6   # ESP32 C6
]

ANTICIPATION = 0.7  # secondes AVANT le beat


# Récupération des beats avec librosa
def load_beats(audio_path):
    y, sr = librosa.load(audio_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return beat_times

# Envoi de la vibration à l'ESP32
def envoyer_vibration(index):
    esp = ESP32_CONFIG[index % len(ESP32_CONFIG)]
    try:
        requests.post(f"{esp}/vibrate", timeout=1)
        print(f"🔔 Vibration envoyée → {esp}")
    except:
        print(f"⚠️ ESP32 non joignable : {esp}")

# Vérification du mouvement détecté par l'ESP32 (accéléromètre)
def mouvement_detecte(esp_ip):
    try:
        r = requests.get(f"{esp_ip}/movement", timeout=1)
        if r.status_code == 200:
            return r.json().get("mouvement", False)
    except:
        pass
    return False

# Calcul des étoiles en fonction du score
def calculer_etoiles(score, total):
    tiers = total / 3
    if score <= tiers:
        return 1
    elif score <= 2 * tiers:
        return 2
    else:
        return 3

# Vérification du mouvement dans une fenêtre de temps
def verifier_mouvement(esp_ip, window_end, result):
    """Poll l'ESP32 jusqu'à la fin de la fenêtre pour détecter un mouvement"""
    success = False
    check_interval = 0.05
    while time.time() < window_end:
        if mouvement_detecte(esp_ip):
            success = True
            break
        time.sleep(check_interval)
    result["success"] = success

# Fonction du lancement du jeu

def lancer_jeu(musique_path, niveau):
    print("\nInitialisation du jeu...")


    # Initialisation musique
    pygame.mixer.init()
    pygame.mixer.music.load(musique_path)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()

    # Analyse des beats
    beat_times = load_beats(musique_path)
    nb_beats = len(beat_times)

    score = 0
    esp_nb = 0
    t0 = time.time()

    for i, beat_time in enumerate(beat_times):
        # Calcul du moment exact pour le beat
        moment = t0 + beat_time - ANTICIPATION
        sleep_time = max(moment - time.time(), 0)
        time.sleep(sleep_time)

        # Déclenchement vibration tous les 4 beats
        esp_ip = None
        if i % 4 == 0:
            esp_ip = random.choice(ESP32_CONFIG) # choix aléatoire de l'ESP32
            print(f"\nBeat {i} → vibration ESP32 {esp_ip}")
            envoyer_vibration(ESP32_CONFIG.index(esp_ip))

        # Fenêtre de validation
        if i + 2 < nb_beats:
            window_end = t0 + beat_times[i + 2]
        else:
            window_end = t0 + beat_times[-1] + 1.0

        success = False

        # Vérification du mouvement si une ESP32 a été activée
        if esp_ip:
            esp_nb += 1
            result = {}
            thread = Thread(target=verifier_mouvement, args=(esp_ip, window_end, result))
            thread.start()
            thread.join()  # on attend la fin de la fenêtre
            success = result.get("success", False)

            if success:
                score += 1
                jouer_succes()
                print("✔ Réussi")
            else:
                jouer_erreur()  # décommenter si tu veux un son erreur
                print("✘ Raté")

        # Stop si musique terminée
        if not pygame.mixer.music.get_busy():
            break

    pygame.mixer.music.stop()

    # Fin de la partie
    etoiles = calculer_etoiles(score, esp_nb)
    parler(f"Bravo, vous avez obtenu {etoiles} étoiles.")

    for _ in range(etoiles):
        jouer_etoile()
        time.sleep(0.4)

    parler(f"Votre score est de {score} sur {esp_nb}.")

    # Menu fin de partie
    while True:
        parler(
            "Appuyez sur 1 pour rejouer cette musique. "
            "Appuyez sur 2 pour revenir au choix du niveau. "
            "Appuyez sur Q pour quitter. "
            "Appuyez sur 0 pour répéter."
        )

        print("1 - Rejouer la musique")
        print("2 - Retour au choix du niveau")
        print("Q - Quitter")
        print("0 - Répéter")

        choix = input("Votre choix : ").strip().lower()

        if choix == "1":
            return "rejouer"
        elif choix == "2":
            return "niveau"
        elif choix == "q":
            parler("Merci d'avoir joué. À bientôt.")
            exit(0)
        elif choix == "0":
            continue
        else:
            parler("Choix invalide.")

