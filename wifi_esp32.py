"""
Module de gestion de la connection des ESP32 en WiFi
"""
import requests
import time
from tts import parler

import requests

IP_S3 = "http://192.168.137.71"
IP_C6 = "http://192.168.137.116"

# !!!!!! IP à changer en fonctiont des adresses des ESP32 sur le réseau local !!!!!!!

requests.post(f"{IP_S3}/vibrate", data="1", timeout=1) # Envoie une vibration à l'ESP32 S3
print("envoyé S3")

requests.post(f"{IP_C6}/vibrate", data="1", timeout=1) # Envoie une vibration à l'ESP32 C6
print("envoyé C6")


ESP32_LIST = {
    "Bracelet gauche": IP_S3, # ESP S3
    "Bracelet droit": IP_C6 # ESP C6
}

TIMEOUT = 0.5


def tester_esp32():

    tout_ok = True

    for nom, ip in ESP32_LIST.items():
        try:
            r = requests.get(f"{ip}/ping", timeout=TIMEOUT)
            if r.status_code == 200:
                parler(f"{nom} connecté.")
                print(f"✅ {nom} OK")
            else:
                parler(f"{nom} ne répond pas.")
                print(f"❌ {nom} ERREUR")
                tout_ok = False

        except:
            parler(f"{nom} non détecté.")
            print(f"❌ {nom} non joignable")
            tout_ok = False

        time.sleep(0.3)

    return tout_ok
