"""
Module de Text-To-Speech (synthèse vocale)
"""

import pyttsx3

def parler(texte):
    engine = pyttsx3.init()   # moteur recréé à chaque fois
    engine.setProperty('rate', 200) # Vitesse de la parole
    engine.say(texte)
    engine.runAndWait()
    engine.stop()
 