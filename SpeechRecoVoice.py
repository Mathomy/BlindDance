#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 16:47:20 2025

@author: camelia
"""

import speech_recognition as sr

# Création de l'objet Recognizer
r = sr.Recognizer()

# Choisir le micro MacBook Air (index 0)
mic_index = 0

# Boucle infinie pour écouter en continu
while True:
    with sr.Microphone(device_index=mic_index) as source:
        print("Parlez quelque chose...")
        # Ajuster le bruit ambiant
        r.adjust_for_ambient_noise(source, duration=1)
        # Écouter le micro
        audio = r.listen(source)

    try:
        # Reconnaissance vocale via Google
        text = r.recognize_google(audio, language="fr-FR")
        print("Vous avez dit :", text)

        # Vérifier le mot clé
        if "quitter" in text.lower():
            print("quitter")
            break  # sortir de la boucle

    except sr.UnknownValueError:
        print("Je n'ai pas compris, répétez...")
    except sr.RequestError as e:
        print("Erreur API Google Speech :", e)
